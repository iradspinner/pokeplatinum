# The Battle Zone before the Elite Four

Scoping note, 2026-09-25, from the encounter track at Ian's request. Ian wants
the Battle Zone (the Fight Area, Routes 225 to 230, the Survival Area, the
Resort Area and Stark Mountain) open before the League, as Platinum Kaizo has
it, for the fights and the captures it adds. Ian ruled on the three open
questions the same day (below). The main and encounter tracks' parts are
done and merged; the balance track's re-levelling is what is left, in the
tracker's Battle Zone entry.

## Current state (2026-09-27; read this first)

Parts of this plan were overtaken on 2026-09-26, and the tracker's Battle Zone
entry is the current word. The zone opens **after Galactic HQ**, not after Lake
Acuity, and the Galactic stretch is two splits: **HQ, cap 60**, then
**Galactic, cap 65**. The ferry's sailor has **one** `FLAG_GAME_COMPLETED`
check, not two (the other two guard Snowpoint Temple, which stays post-game),
and it now tests Galactic HQ being cleared. The Fight Area's block on Route
225 lifted only after the Volkner and Flint tag battle; since that battle now
waits for the Beacon Badge, Route 225 is open from the player's first arrival
and the ferry is the only gate. Ruling 2 below is replaced too: Stark
Mountain's last room holds **no legendary** for now, Heatran included, and no
draw (Ian, 2026-09-27), until the difficulty is high enough that more
legendary-tier encounters would not inflate box quality. The main track did
all this on `main-scripts`, merged: the ferry tests
`FLAG_FREED_GALACTIC_HQ_POKEMON`, and the Fight Area's Beacon Badge gate and
lines are in (3a3472432); Stark Mountain's last room hides Heatran on every
load (ba09950fa). The tracker archive's Battle Zone entry has each sub-item.

## Ian's rulings (2026-09-25)

1. **A new split, Galactic, straight after Lake Acuity.** It holds the whole
   Battle Zone and the Galactic fights up to the Distortion World (the Veilstone
   HQ, the Mt. Coronet climb, Spear Pillar), which spreads those fights out. Its
   cap is **64**; Candice's stays **56** and Volkner's rises from 62 to **68**.
   The League stays 78.
2. **Heatran becomes a random legendary encounter**, as Uxie and Azelf are:
   Stark Mountain's last room joins the legendary pool's statics.
3. **The Battleground rematches are skipped for now**, to come back to.

## What gated it in the base ROM, before `main-scripts`

The only way in is the ferry from Snowpoint City. Its sailor checks two
things: the National Dex, which this game grants at the start (the Sandgem lab
turns it on with the Pokédex, a base ROM change), and `FLAG_GAME_COMPLETED`,
which only the Hall of Fame sets. The sailor checks that flag once; the
other two checks in `scripts_snowpoint_city.s` guard Snowpoint Temple. Past the ferry nothing else asks whether the game is complete,
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
the League are post-game content and can stay. `main-scripts` reworded the
rest; the new lines are drafts waiting on Ian (the tracker's "Drafts from
`main-scripts`").

## The work, by track

Main track: done on `main-scripts` and merged, to the placement after Galactic
HQ (see "Current state"); the tracker archive's Battle Zone entry has each
sub-item with its commit.

Balance track: the caps and the re-levelling, in the tracker's Battle Zone
entry, which has the current numbers (this plan's were for a Galactic cap of
64).

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
   vanilla's Battle Zone sits above it. (Moot since 2026-09-30: no HQ or
   Galactic table holds Metagross or a fully evolved starter; the OxiDex
   Agent checked.) Two things they offered before Volkner were Ian's call: Metagross at 10% on Route 228, and the fully evolved starters
   as 1% tails (Blaziken, Incineroar, Charizard, Serperior and Meowscarada on
   land; Greninja, Primarina, Blastoise and Swampert on the Super Rod).
3. The capture count before the League: 73 planned, 81 with the zone's eight
   capture areas, once the ferry opens.

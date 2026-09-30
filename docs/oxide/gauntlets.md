# The gauntlets

Attrition lives in gauntlets (Ian, 2026-09-27). The Pocket PC heals anywhere
except in chosen one-way stretches of the game's dungeons, where the player
beats a run of trainers before leaving to heal. The balance plan chose twelve
sections, and Ian took all twelve. On 2026-09-29 he ruled how they work. A
section blocks only its way back, so a player may push on without beating
everyone. While it is open, the Pocket PC, the Escape Rope and Dig refuse. It
closes when the player leaves by the way forward, or has beaten all its listed
trainers. Ian judges the trainers above their split's average case by case, so
the trainer lists below are today's and will change.

This file records how the gauntlets are built and why each map and warp is in
its section. The code is `src/gauntlet.c`; the in-game checks are in
`docs/oxide/ingame-checklist.md`, sections 2 (the test kit's five gauntlet
warps) and 4.

## How it works

One saved variable, `VAR_GAUNTLET_SECTION`, holds the open section's number,
or 0 when none is open. It takes vanilla's unused variable 0x408F, so nothing
in the save moves and no new game is needed.

A section opens when the player arrives through one of its ways in, provided
one of its listed trainers is still to beat. A trainer counts only while
unbeaten and on the map: the story hides some sections' trainers before or
after their part (the Eterna grunts once Jupiter falls, Mt. Coronet's once
the Sendoff Spring scene plays), and a section must never wait on a trainer
the player cannot reach. The section stays open while the player is on one of
its maps. Those include the dead-end pockets a detour reaches, so that
stepping into a side room does not close it. Arriving on any other map closes
it. That covers the way forward, a scripted warp and a whiteout alike.

While a section is open:

- a warp listed as one of its ways back is refused, with the message below.
  This covers doors, stairs, cave entrances and warp panels; after a step
  onto the warp's tile the player is walked back off it;
- the Pocket PC and the Escape Rope refuse, with their own message in the bag;
- Dig, Fly and Teleport refuse, with their own message in the party menu. Fly
  and Teleport are added to Ian's list because two of Mt. Coronet's maps
  inside a section are outdoors, where both work.

Galactic HQ 3F's way back is refused only while the player holds the Galactic
Key. Its way on is a locked door, and a player who skipped the key on B2F
would otherwise be shut in.

Victory Road 1F holds two sections on one map. A line across a one-tile
corridor at (13,26) and (13,27) splits them: three coord events run the
field moves archive's line script. Stepping onto (13,26) facing north opens
the far section. Stepping onto (13,27) facing south while the far section is
open turns the player back.

## The back blocks

Every back block is a refused warp, apart from Victory Road's line. Ian
suggested a one-way ledge where the map allows one. None of the ways back
crosses an existing ledge that points the right way: Victory Road's ledges
drop toward its entrance, so they would block the way forward, not back. A
new ledge means editing the map's 3D model, not just its tiles.

## The sections

Each area was walked with a model of its tiles: collision, one-way ledges,
Rock Climb walls, bridges (a bridge's deck and the floor under it are kept
apart) and the key doors shut. Strength boulders and Rock Smash rocks are not
modelled, which matters only on Victory Road 2F.

| # | Section | Trainers | Way in | Ways back, refused | Way forward | Lock also holds on |
|---|---|---|---|---|---|---|
| 1 | Eterna building 1F and 2F | the 1F grunts, the 2F grunts | the front door from Eterna City | the front door | 2F's stairs to 3F's main side | 3F's dead-end pocket, Rotom's room |
| 2 | Eterna building 3F | Travon, the 3F grunt | the stairs from 2F's main side | those stairs | the stairs to Jupiter on 4F | |
| 3 | Galactic HQ B2F | the two B2F grunts | from the Veilstone warehouse | back to the warehouse | on to B1F | |
| 4 | Galactic HQ 1F | the 1F grunt, Fredrick | from B1F | back to B1F, and the lobby's two front doors | the panels and stairs to 2F | |
| 5 | Galactic HQ 2F | the four 2F trainers | the stairs from 1F's panel room | those stairs | the stairs to 3F | Fredrick's pocket on 1F, and B2F's dead end past it |
| 6 | Galactic HQ 3F | the four 3F grunts | the stairs from 2F | those stairs, while the Galactic Key is held | past the key door, the stairs to Cyrus on 4F | 2F's east side and the hall, reached from 3F |
| 7 | Mt. Coronet 1F's tunnel | the three tunnel grunts | from Route 211's north room | back to that room | out to the north ledge | |
| 8 | Mt. Coronet 3F to 5F | the 3F and 4F grunts, Somnu | the stairs from 2F | those stairs, and the north ledge's cave mouth into the tunnel | 5F's stairs to 6F | the outside ledges, 4F's rooms, 2F's pocket |
| 9 | Victory Road, near half | Bryce, Hana, Mariah | from the League's south gate | back to the gate | north across the line | 2F and B1F |
| 10 | Victory Road, far half | Miles, Clinton, Edgar | across the line | south across the line, and the back rooms' exit to Route 224 | the exit to the League | 2F, B1F, the back rooms |

## Where the walk differs from the balance plan's sections

The balance plan drew its sections floor by floor. Walking the maps changes
five things.

| Area | What the walk shows | What was built |
|---|---|---|
| Galactic HQ | The warehouse leads into B2F, so the HQ is walked B2F, B1F, 1F, 2F, 3F, and B2F comes first. | Sections 3 to 6 in that order. |
| Galactic HQ 1F | The route passes only the grunt. Fredrick stands in a pocket reached only by coming down from 2F. | Fredrick stays in section 4's list, so that section closes only when the player moves on to 2F. |
| Galactic HQ 2F | The route passes only one grunt. Darrius and the other two stand on 2F's east side, reached from 3F through the hall. | They stay in section 5's list; section 6's lock holds on that detour, so a player there cannot heal. |
| Mt. Coronet | Two climbs meet on the north ledge: the tunnel from Route 211, and the southern route through 3F and 4F. Somnu on 5F comes after both. | Only the southern route opens section 8; a player who takes the tunnel meets Somnu outside any section. |
| Victory Road | 1F alone runs from the entrance to the exit. 2F is a Strength-puzzle loop off 1F's near half; B1F's main part is a dead end off the same stretch; Ondrej stands in a separate B1F pocket off the far half. | Blocking a way back on 2F or B1F could shut a player in, so they are detours inside the 1F sections' locks, not sections of their own, and their eight trainers are optional. The four Victory Road sections become two. |

On Victory Road 1F the walk passes Bryce and Hana, then Mariah and Miles, then
Edgar, then Clinton, so no line puts Miles with Clinton and Edgar. The line
sits after Miles. The far half's list keeps today's three, so unless Miles was
beaten before the line, the far half closes only at the exit. Moving him to the
near half's list is one line in `src/gauntlet.c`.

## Wording, drafts for Ian

| Where | Text |
|---|---|
| A refused way back, in the field | There’s no turning back now! / Press on, or beat the Trainers here. |
| The Pocket PC or the Escape Rope, in the bag | You can’t use that here yet! / Press on, or beat the Trainers here. |
| Dig, Fly or Teleport, in the party menu | You can’t use that here yet! / Press on, or beat the Trainers here. |

Each line fits the widest line its window already shows.

## Changing a section

A section is one entry in `sGauntletSections`: its maps, its ways in, its ways
back (each with an optional item the player must hold for the refusal to
apply), and up to five trainers with the flags that hide them. A warp is named
by its map and its index in the map's events file. `tools/oxide/mapreach.py`
walks a map, or a set of them, and prints which warps and trainers each pocket
reaches, so a change can be checked against the geometry first.

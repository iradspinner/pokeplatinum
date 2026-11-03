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

Named Galactic officers stay outside every gauntlet, so the player can heal
before each of them (Ian, 2026-10-31: "No, they should not be in gauntlets,
apologies if that is countermanding a previous statement but it would be too
hard to manage the difficulty"). Section 8 now ends on arrival at Mt. Coronet
5F, before Officers Somnu and Moira. Section 2, the Eterna building's 3F, is
gone (Ian, 2026-10-31, approving `story-route.md`'s proposal): without Officer
Moira it would have held Scientist Travon alone, under the 2 to 5. Section 1
now ends on arrival at 3F's main side, so Travon and Moira are both fought
with healing allowed. The stairs arrive at (2,3), outside both sight lines:
Travon looks east along row 9 from (3,9), and Moira north from (16,5). Section 2's number stays unused, so the later sections
keep theirs.

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
it. That covers the way forward, a scripted warp and a whiteout alike. Where
the way forward leads onto a map that also holds one of the section's
pockets, arriving through that warp closes the section too (`sGauntletExits`
in the code); the Eterna building's 3F is the one case.

While a section is open:

- a warp listed as one of its ways back is refused, with the message below.
  This covers doors, stairs, cave entrances and warp panels; after a step
  onto the warp's tile the player is walked back off it;
- the Pocket PC and the Escape Rope refuse, with their own message in the bag;
- Dig, Fly and Teleport refuse, with their own message in the party menu. Fly
  and Teleport were added because two of Mt. Coronet's maps inside a section
  are outdoors, where both work, and Ian kept them (2026-09-29).

The Galactic HQ holds two sections since 2026-11-02 (Ian's answer that day
to `docs/oxide/hq-split-map.md`, question 4), drawn on the HQ's real walk.
The HQ is two halves that share no tile. The basement run goes from the
warehouse down into B2F, then B1F, 1F's back rooms, 2F's west side (3F's
west side a detour off it), Fredrick's room and B2F's north end, where the
Galactic Key lies; its way on is back out through the warehouse. With the
key the player walks round to the HQ's front door in Veilstone and opens the
lobby's inner door, which leads up into the tower: 2F's east side, the hall
and Cyrus's speech, the nap room on 2F's north-east side, 3F's east side,
and the stairs to Cyrus on 4F.

Section 3 is the basement run. It opens on arrival in B2F from the
warehouse, lists B2F's two grunts, B1F's grunt, 1F's grunt and Scientist
Fredrick, and holds all five floors, so every pocket the run reaches keeps
the lock. Its way back, the warp to the warehouse, is refused only until the
player holds the Galactic Key: the reverse of the item test the code had,
written as a second field on the warp (`untilHeldItem`). A player who comes
back in with the key, for 3F west's locked room, can always walk out.
Arriving in the warehouse closes it.

Section 6 is the tower. It was 3F's east side alone from earlier on
2026-11-02 and grew down to the lobby's stairs, so the two sections for the
tower became one. It opens on arrival on 2F from the lobby's stairs, refuses
those stairs, and lists 2F's grunt pair, Scientist Darrius and 3F's grunt
pair. Arriving on 4F closes it. While it is open the nap room's bed refuses
too, as the Pocket PC does, through a new script command, `GauntletIsOpen`.
Sections 4 and 5 are empty, so that the later sections keep their numbers.
The named officers stand outside both sections: Phobos and Deimos in the
lobby before the tower opens, Boreas and Laverna on 4F before Cyrus, Argo on
4F after him, and Hesperid in the laboratory.

Until 2026-11-02 the HQ was read as one climb, B2F to 3F, with 3F's locked
door leading on to 4F. In fact that door opens only a room off 3F's west
side. Section 6 then opened on 2F's west stairs and refused them while the
player held the Galactic Key, with 3F's east grunts in its list, so a player
who came back to 3F west with the key could never close it.
`test_b1e`'s no-trap check walks every section from each way in and from
every place inside it, with and without the key, and fails if a place has
neither a way off the section's maps nor every trainer that closes it.

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
| 1 | Eterna building 1F and 2F | the 1F grunts, the 2F grunts | the front door from Eterna City | the front door | 2F's stairs to 3F's main side, which close it on arrival | 3F's dead-end pocket, Rotom's room |
| 2 | none since 2026-10-31 (it was the Eterna building's 3F, with Travon and Officer Moira) | | | | | |
| 3 | Galactic HQ, the basement run | B2F's two grunts, B1F's grunt, 1F's grunt, Fredrick | from the Veilstone warehouse | back to the warehouse, until the Galactic Key is held | back out to the warehouse with the key | B1F, 1F's back rooms, 2F and 3F's west sides, B2F's north end |
| 4 | none since 2026-11-02 (it was 1F) | | | | | |
| 5 | none since 2026-11-02 (it was 2F) | | | | | |
| 6 | Galactic HQ, the tower | 2F's grunt pair (2 and 3), Darrius, 3F's grunt pair (3 and 4) | the lobby's stairs up to 2F | those stairs | the stairs to Cyrus on 4F | the hall, the nap room (whose bed refuses), 3F's east side |
| 7 | Mt. Coronet 1F's tunnel | the three tunnel grunts | from Route 211's north room | back to that room | out to the north ledge | |
| 8 | Mt. Coronet 3F and 4F | the 3F and 4F grunts | the stairs from 2F | those stairs, and the north ledge's cave mouth into the tunnel | 4F's third room's stairs to 5F | the outside ledges, 4F's rooms, 2F's pocket |
| 9 | Victory Road, near half | Bryce, Hana, Mariah | from the League's south gate | back to the gate | north across the line | 2F and B1F |
| 10 | Victory Road, far half | Miles, Clinton, Edgar | across the line | south across the line, and the back rooms' exit to Route 224 | the exit to the League | 2F, B1F, the back rooms |

## Where the walk differs from the balance plan's sections

The balance plan drew its sections floor by floor. Walking the maps changes
five things.

| Area | What the walk shows | What was built |
|---|---|---|
| Galactic HQ | Two halves sharing no tile: the basement run from the warehouse to the Galactic Key and back out, and the tower from the lobby to 4F (corrected 2026-11-02). | Section 3 for the basement run, section 6 for the tower; sections 4 and 5 empty. |
| Galactic HQ 1F and 2F | Fredrick and Darrius stood off the path; since 2026-11-02 each stands at a neck of his room, so both are required. | Fredrick in section 3's list, Darrius in section 6's. |
| Galactic HQ 3F | The west side, off 2F's west stairs, is a dead end holding grunts 1 and 2 and the locked room with the Ability Capsule; the east side, off the nap room's stairs, holds grunts 3 and 4 on the way to 4F. | Grunts 1 and 2 are optional and in no list; the west side keeps section 3's lock while it is open. |
| Mt. Coronet | Two climbs meet on the north ledge: the tunnel from Route 211, and the southern route through 3F and 4F. Somnu and Moira on 5F come after both. | Only the southern route opens section 8, and it ends on arrival at 5F (2026-10-31), so both climbs meet the officers outside any section. 5F's arrival at (21,7) is nine rows from the nearer sight line, Somnu's on row 16, so the player can heal first. |
| Victory Road | 1F alone runs from the entrance to the exit. 2F is a Strength-puzzle loop off 1F's near half; B1F's main part is a dead end off the same stretch; Ondrej stands in a separate B1F pocket off the far half. | Blocking a way back on 2F or B1F could shut a player in, so they are detours inside the 1F sections' locks, not sections of their own, and their eight trainers are optional. The four Victory Road sections become two (Ian, 2026-09-29). |

On Victory Road 1F the walk passes Bryce and Hana, then Mariah and Miles, then
Edgar, then Clinton, so no line puts Miles with Clinton and Edgar. The line
sits after Miles. The far half's list keeps today's three, so unless Miles was
beaten before the line, the far half closes only at the exit. Ian kept him in
the far half (2026-09-29).

## Wording

Ian approved both messages as drafted (2026-09-29).

| Where | Text |
|---|---|
| A refused way back, in the field | There’s no turning back now! / Press on, or beat the Trainers here. |
| The Pocket PC or the Escape Rope, in the bag | You can’t use that here yet! / Press on, or beat the Trainers here. |
| Dig, Fly or Teleport, in the party menu | You can’t use that here yet! / Press on, or beat the Trainers here. |

Each line fits the widest line its window already shows.

## Changing a section

A section is one entry in `sGauntletSections`: its maps, its ways in, its ways
back (each with an optional item the player must hold for the refusal to
apply, and another whose holding lifts it), and up to five trainers with the
flags that hide them. A warp is named
by its map and its index in the map's events file. `tools/oxide/mapreach.py`
walks a map, or a set of them, and prints which warps and trainers each pocket
reaches, so a change can be checked against the geometry first.

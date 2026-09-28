# Phase 4: Ian's answers to the engine-change questions

Written 2026-09-20. Ian answered the ten Phase 4 engine-change questions one at
a time, with follow-ups where an answer opened a second decision. Each answer
restates what it was asked; the questions file was removed in the 2026-09-21 docs
pass.

## 1. The answers

**1. Items: a curated subset, chosen by category, added into Platinum's existing
table.** Not the whole 2,687-record table, and not "none". The item table stays
Platinum-shaped; new items go into free slots (widen the table only if the list
below outgrows the free slots). Ian judged categories as a whole rather than
individual items. Gems are an explicit no.

In:

- Core Gen 5-6 held items: Eviolite, Air Balloon, Rocky Helmet, Assault Vest,
  Weakness Policy, Safety Goggles, Red Card, Eject Button, Ring Target, Binding
  Band, Absorb Bulb, Cell Battery.
- Terrain and seed items: Terrain Extender, Electric/Grassy/Misty/Psychic Seed.
  (Ian ruled on 2026-09-27 that terrain is not ported, so these have nothing
  to react to; the tracker's Phase 5 has the ruling.)
- Gen 9 held items: Booster Energy, Covert Cloak, Clear Amulet, Mirror Herb,
  Loaded Dice, Punching Glove, Ability Shield, Fairy Feather. Booster Energy only
  does anything if a Paradox species with Protosynthesis/Quark Drive is in the
  pick-list; check before implementing it, and drop it if none is.
- Ability Capsule and Ability Patch (see Q5).
- Mints (nature setting).
- Bottle Cap and Gold Bottle Cap (Hyper Training). Needs the summary-screen
  EV/IV viewer to reflect hyper-trained IVs, or the two features will disagree.
- Fairy-type support: Pixie Plate (Arceus/Judgment), Roseli Berry.
- New TMs for the new moves. **Ian's note: 92 TMs might not be enough, and TMs
  need a larger pass when balance is done as a whole.** Treat "how many TMs and
  which moves" as a Phase 5 / balance item; for Phase 4, the mechanism for more
  than 92 TMs is what matters, so the TM count should not be hard-capped by the
  port.

Out: Gen 7-8 held items (Protective Pads, Adrenaline Orb, Throat Spray, Eject
Pack, Heavy-Duty Boots, Blunder Policy, Room Service, Utility Umbrella); Exp.
Candies (redundant with chained Rare Candies); new evolution items (Ice Stone,
Linking Cord, apples, pots, Galarica items, etc.; the pick-list's stand-in
methods stay as they are); extra Poke Balls (HGSS Apricorn balls, Dream Ball,
Beast Ball); Gems; Mega Stones (see Q4).

Each held item that is in needs its battle effect written into Platinum's
engine, with hg-engine's C as the reference, and the AI made aware of it where
it changes a decision (Eviolite, Assault Vest, Air Balloon, Rocky Helmet at
least). That AI awareness belongs in the battle-AI work, not the item work.

**2. Evolution methods: only what the pick-list uses.** Every method in the
pick-list already exists in Platinum (friendship, level, stone, level-up holding
an item by day/night, level-up knowing a move, level-up female, magnetic field),
so nothing new is coded now. Hardlove's 19 extra methods are not ported. If a
later species needs one, add that one method then.

**3. Evolution slots: 9 per species, and strip the 17 dead trade entries.** The
deciding case is Eevee: Platinum's seven slots are full (Vaporeon, Jolteon,
Flareon, Espeon, Umbreon, Leafeon, Glaceon) and Sylveon makes eight. The record
widens to Hardlove's 56-byte / 9-slot layout and `evo.narc` is rebuilt. The
seventeen unreachable trade evolutions (methods 5 and 6) the base ROM left
beside its non-trade routes are removed too. Both are done: the nine slots
landed with element 3, the strip with element 8 (tracker archive).

**4. Mega Evolution: no.** Gyarados M and Lopunny M are ordinary permanent
evolutions and that is the whole of it. No Mega Stones, no battle UI, no
transformation code. Any future Mega follows the same alt-evolution pattern.

Follow-up, the triggers the pick-list left TBD: **level-up holding a stone-like
item, entered twice as methods 18 (day) and 19 (night)**, matching the base
ROM's convention. Ian left the item choice open; the proposed defaults, Dragon
Scale for Gyarados M and Fist Plate for Lopunny M (both already in Platinum),
are what the species port put in `res/pokemon/gyarados` and `lopunny`.

**5. Hidden abilities: yes, the full mechanic.** Third ability slot per species
from Hardlove's `a/0/2/8`-style table, the script flag that lets chosen
encounters roll it, and Ability Patch as the player-facing route to it. Which
encounters set the flag (gifts, statics, a late area) is a Phase 5 encounter
design decision, not a Phase 4 one.

Follow-up, the 228 duplicated second-ability slots from the base ROM: **keep
them as they are for now.** A single-ability species stays single-ability; just
add the hidden slot. **Ian's note: a larger ability balance pass will be needed
later.** Log it as a Phase 5 item alongside the TM pass.

**6. Experience formula: keep Platinum's.** The flat Gen 4 formula stays; the
base ROM's trainer curve was tuned against it and Rare Candies handle any grind.
The Gen 5/7 level-scaled toggle is not taken.

**7. Save format: break it freely; PKHeX compatibility does not matter.** Fresh
saves only, and the layout changes as each feature needs. This was already true
in practice once species IDs pass 493 and ability IDs pass 123. **Ian's note: an
optional add-on to this project is a local build of PKHeX/PKHaX dedicated to
this ROM.** Not scoped, not scheduled; record it in the backlog so the save
layout is documented well enough to make that possible (a short
`docs/oxide/save-layout.md` listing every block that moved and why would be
enough).

Follow-up: **30 PC boxes**, up from Platinum's 18. A living dex of 652 needs 22.

**8. Quality-of-life toggles.**

In:

- Always-set battle mode. Note the base ROM's trainers were balanced with Shift
  available; the Phase 5 balance pass should assume Set.
- 60 fps outside battle, matching the battle uncap already carried over.
  hg-engine flags the overworld version as less stable; if it misbehaves, drop it
  without asking.
- Wild double battles. Needs per-area configuration (Phase 5 encounter design)
  and the AI handling doubles well, which ties into the AI work below.
- Restore single-use items after battle (berries, Focus Sash, Weakness Policy,
  seeds and the rest come back). Fits the timewaster principle.
- Always national dex. The curated 360 dex is a presentation layer on top, so
  this means the full listing is visible from the start too; the dex ordering
  work in the species port should assume that.
- Level caps driven by a script variable. Combined with chained Rare Candies
  this is what makes "candy to the cap, no grinding" work. **Ian's note: level
  caps and their associated "splits" should be thoroughly defined, with the
  areas, trainers, available items, and learnsets/evolutions associated with each
  split. This will likely take a lot of work.** Phase 4 delivers the mechanism
  (the variable, the exp gate, the script command to raise it). The split
  definitions are a design document of their own, in Phase 5, and should be
  written before the trainer balance pass since they constrain it.
- Lowered friendship evolution threshold (hg-engine's option; use its default
  lowered value unless a specific number is wanted). Affects Alomomola,
  Frosmoth, Espeon/Umbreon, Riolu, Golbat, Chansey and the other friendship lines.
  Superseded: the friendship evolutions are being replaced in Phase 5 (tracker,
  element 8).
- Fast text by default (already true in the base ROM; keep it).

Out: transparent textboxes; capture experience; critical capture; static HP bar.

**HP bar speed, replacing the static-bar toggle.** Ian does not want the HP bar
frozen; he wants it faster. He believes Platinum Unlocked was hex-edited to a
roughly 2x HP-bar drain speed, the well-known community edit for Platinum's
famously slow bars, and wants that carried into Oxide. Found in the base ROM on
2026-09-20, as he expected: ov16 `+0x2D046` in `UpdateGauge` doubles the drain.
Ported as a base-ROM carry-over at the HP call site, since the patched
instruction is shared with the EXP gauge (tracker archive, Phase 4).

**9. Learnset format: confirmed, widen it** to (u16 level, u16 move). Required
for any level-up learnset containing a move above ID 511.

**10. Followers: deferred, maybe later.** Out of Phase 4. The overworld sprite
import during the species port should be complete enough (all species, not just
the ones Platinum shows in the overworld) that a follower system could be added
later without redoing the sprite work.

## 2. What this changed in the scope table

The scope table is the design doc's section 3, and the element order is the
tracker's Phase 4: 1 Fairy, 2 the ability widening, 3 species slots, 4 moves,
5 ability effects, 6 the battle AI, 7 items, 8 the rest of this list.

## 3. New Phase 5 / backlog items Ian raised while answering

All five (the TM pass, the ability balance pass, the level-cap split design,
an optional ROM-specific PKHeX build, and the hidden-ability and wild-double
encounter decisions) are entries in the tracker's Phase 5.

## 4. Battle AI

The approach Ian set for element 6, and what these answers added to it (the
held items that change a decision, and doubles scoring getting the same
scrutiny as singles), are in the tracker's element 6 entry and
`docs/oxide/battle-ai/README.md`.

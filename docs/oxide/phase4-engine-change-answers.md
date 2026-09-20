# Phase 4: Ian's answers to the engine-change questions

Written 2026-09-20. Ian answered the ten questions in
`phase4-engine-change-questions.md` one at a time, with follow-ups where an
answer opened a second decision. Format follows `phase3-answers-and-trainer-format.md`.

Claude Code should fold these into `docs/oxide/design-doc.md` (scope table,
engine-change list) and `docs/oxide/tracker.md`, and keep this file as the record.

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
  (Terrain-setting moves and abilities are coming with the move and ability
  ports, so these have something to react to.)
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
beside its non-trade routes are removed in the same pass.

**4. Mega Evolution: no.** Gyarados M and Lopunny M are ordinary permanent
evolutions and that is the whole of it. No Mega Stones, no battle UI, no
transformation code. Any future Mega follows the same alt-evolution pattern.

Follow-up, the triggers the pick-list left TBD: **level-up holding a stone-like
item, entered twice as methods 18 (day) and 19 (night)**, matching the base
ROM's convention. Ian left the item choice open; proposed defaults are Dragon
Scale for Gyarados M and Fist Plate for Lopunny M (both already in Platinum).
Change them if a better thematic fit turns up during the species port.

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
- Fast text by default (already true in the base ROM; keep it).

Out: transparent textboxes; capture experience; critical capture; static HP bar.

**HP bar speed, replacing the static-bar toggle.** Ian does not want the HP bar
frozen; he wants it faster. He believes Platinum Unlocked was hex-edited to a
roughly 2x HP-bar drain speed, the well-known community edit for Platinum's
famously slow bars, and wants that carried into Oxide. Claude Code should locate
it in the base ROM before assuming the value: the Phase 3 inventory recorded
unexplained small edits in ov16 (`+0xEA3C`, `+0x10D58`, `+0x2D046`, and a
4-entry table at `+0x1309C..+0x130BE` changed from 10/30/50/70 to 255), and one
of those is a candidate. If it is found, port the same constant; if it is not,
implement a 2x drain in C directly. Either way this is a base-ROM carry-over
item, not a new feature.

**9. Learnset format: confirmed, widen it** to (u16 level, u16 move). Required
for any level-up learnset containing a move above ID 511.

**10. Followers: deferred, maybe later.** Out of Phase 4. The overworld sprite
import during the species port should be complete enough (all species, not just
the ones Platinum shows in the overworld) that a follower system could be added
later without redoing the sprite work.

## 2. What this changes in the scope table

Phase 4 order stays: Fairy type, ability widening (now including the hidden
slot), move expansion (with the widened learnset format), species slots (9-slot
evo records, 30 boxes, expanded dex flags), battle AI. Items slot in after the
move expansion, since several held items reference new moves and abilities.

Cut from the menu for good: whole item table, Gen 8 evolution methods, Megas,
Gen 5/7 exp formula, transparent textboxes, capture exp, critical capture,
static HP bar, extra Poke Balls, new evolution items, Exp. Candies, Gems, Gen 7-8
held items. Followers deferred.

## 3. New Phase 5 / backlog items Ian raised while answering

- TM pass: how many TMs (likely more than 92) and which moves, done with the
  overall balance pass.
- Ability balance pass across all species, including the 228 duplicated slots.
- Level-cap split design: per split, the areas, trainers, items, and
  learnsets/evolutions available. Prerequisite for trainer balance.
- Optional: a ROM-specific PKHeX/PKHaX build. Depends on the save layout being
  documented as it changes.
- Hidden-ability encounter flagging and wild-double areas, both part of
  encounter design.

## 4. Battle AI

Nothing in this pass changes the AI section of the questions doc: read
`src/battle/trainer_ai/` first, write it up to the point where a change can be
predicted, keep fixes separate from behaviour changes, and apply the eleven
`battle_edits` fixes last. Two things from today's answers feed into that
write-up: the AI must understand the new held items that change decisions
(Eviolite, Assault Vest, Air Balloon, Rocky Helmet, Weakness Policy, the seeds),
and wild double battles mean the doubles-specific scoring gets exercised far
more than in vanilla, so it needs the same scrutiny as singles.

# The Pocket PC: the base ROM's Vs. Seeker

Surveyed 2026-09-26 by the Carry-over Agent, from the base ROM's arm9 and its
`scripts_common`, so that Ian could rule on each function before any of it
moved. He ruled on all of it on 2026-09-27; the rulings are the last section,
and they are being built on branch `carry-over`. The survey below describes
the base ROM, not Oxide.

## How it works in the base ROM

The base ROM changed two literals in arm9 and nothing else for this: the
Vs. Seeker's bag and field handlers (`UseVsSeekerFromMenu` and
`UseVsSeekerInField` in `src/item_use_functions.c`) run common script 58
instead of the Vs. Seeker's script. Common script 58 opens the same menu as a
Pokemon Center PC (common script 18), skipping the PC's boot animation. The
item keeps vanilla's usability check, so it works only on outdoor maps; in
caves and buildings the bag says it cannot be used. The player gets it in
Sandgem at the start of the game, with TM10; vanilla gives the Vs. Seeker
later, on Route 207. Its name already reads Pocket PC, from the text
carry-over.

`scripts_common` came over from the base ROM whole, so **every Pokemon Center
PC in the current build already offers everything below**, the free Move
Reminder included. Only the item's hookup is missing, and today the item named
Pocket PC still works as a Vs. Seeker. The hookup is two lines of C. Every
other ruling is an edit to `scripts_common`, and an edit there changes the
Pokemon Center PCs as well unless the menu is taught to tell the two apart: a
flag set by common script 58 and checked by each entry that differs, a few
lines each.

## What it offers

The top menu, in the order it shows:

| Entry | What it does | Shown |
|---|---|---|
| Pokemon Storage | Vanilla's box system | Always |
| (Player)'s PC | Vanilla's item storage and mailbox | Always |
| Oak's PC | Vanilla's PC Pokedex rating | Always |
| Move Tutors | The sub-menu below | Always |
| Teleport System | Warps to Twinleaf, or to any of 18 places whose Abra the player has talked to once: Sandgem, Jubilife, Oreburgh, Floaroma, Eterna, Hearthome, Solaceon, Veilstone, Pastoria, Celestic, Canalave, Snowpoint, Sunyshore, the Pokemon League, Pal Park, the Fight Area, the Survival Area and the Resort Area | Always; each place once registered |
| Healing Waves | Heals the whole party | Always |
| Online Shop | A Poke Mart with the ordinary stock for the badge count | Always |
| Misc. | The sub-menu below | Always |

Move Tutors:

| Entry | What it does | Shown |
|---|---|---|
| Move Reminder | Vanilla's relearner, free, for any Pokemon | Always |
| Move Tutor 1, 2, 3 | Vanilla's three shard tutors; they still charge shards | 3 badges |
| Starter Tutor | Blast Burn, Hydro Cannon or Frenzy Plant, still needing maximum friendship | 5 badges |
| Dragon Tutor | Draco Meteor | 5 badges |

Misc.:

| Entry | What it does | Shown |
|---|---|---|
| Name Rater APP | Renames a Pokemon | Always |
| Hidden Power APP | Says a Pokemon's Hidden Power type | Always |
| Happiness Up | Sets a Pokemon's friendship to the maximum, free | Always |
| Hall of Fame | Vanilla's Hall of Fame viewer | After the League |
| Legendary Reset | Re-arms Giratina, Arceus, Dialga, Palkia, Heatran, Regigigas, Rotom, Uxie, Azelf, Darkrai, Shaymin and the three Regi ruins, and releases the Moltres, Zapdos, Articuno, Mesprit and Cresselia roamers again | After the Champion |
| Superbosses/Gyms Reset | Lets the eight gym leaders and five superbosses be fought again: May (Resort Area), Steven (Stark Mountain), Cyrus (Turnback Cave), and Red and Gold (Mt. Coronet) | After the Champion |
| Trades/Gifts Reset | Makes the four in-game trades, the Eevee and Porygon gifts and the Manaphy Egg available again | After the Champion |

Two things the change takes away. **Vs. Seeker rematches end**, since the item
no longer runs the Vs. Seeker; nothing else in the game calls route trainers
back, and gym leaders return only through the reset above. And the base
ROM's teleporting Abra in each town stays as it is: it is how a place is
registered, and it teleports on its own too.

## What each ruling costs

Everything above already exists in the build, so no entry needs porting; the
work is keeping, dropping or changing entries.

| Change | Size |
|---|---|
| Hook the item up to the menu | Two lines of C |
| Let it work indoors too | One more line of C |
| Drop an entry from every PC | One or two script lines |
| Drop or keep an entry on the Pocket PC only | The flag above plus a check per entry |
| Infinite Rare Candies as a new entry that fills the bag's stack to 999 each time | About ten script lines and one menu text |
| Infinite Rare Candies as a Rare Candy that is never used up | A small C change in the party menu's item use |
| Give the Vs. Seeker back as its own item | A free item slot, element 7's item work |

## Questions put to Ian (answered in the rulings below)

1. Should the Pocket PC work everywhere, or only outdoors as in the base ROM?
2. The Move Reminder leaves the Pocket PC by ruling. Should it leave the
   Pokemon Center PCs too? Recommended: yes, since a free relearner in every
   Pokemon Center would undo the Heart Scale price in Pastoria.
3. How should infinite Rare Candies work, and where? Recommended: a Pocket PC
   entry that fills the bag to 999, on the Pocket PC only.
4. For each other entry, keep it on both, on one, or drop it. Worth weighing:
   Healing Waves and the Online Shop put a Pokemon Center and a Mart on every
   outdoor map from Sandgem on; the Teleport System is Fly from the first town;
   Happiness Up makes every friendship evolution, and the Starter Tutor's
   condition, free; the Legendary Reset re-arms vanilla's legendaries and
   roamers, which the legendary pool (encounter plan, decision 8) has
   replaced; and the Trades/Gifts Reset repeats gifts, which touches the
   nuzlocke capture rules.
5. Vs. Seeker rematches: let them go, or bring the Vs. Seeker back as its own
   item?

## Rulings

Ian ruled on the whole list on 2026-09-27, relayed by the Overseer.

1. **Where it works:** everywhere, caves and buildings included, except in
   gauntlets: one-way areas the player must clear, beating a set number of
   trainers in a row, before leaving to heal. The gauntlets are a later design
   pass; the mechanism is built now, with no map marked.
2. **The item** opens the PC menu. Vs. Seeker rematches go, and no Vs. Seeker
   item comes back.
3. **The Pocket PC keeps** Pokemon Storage, Healing Waves, the Name Rater APP
   and the Hidden Power APP, and gains an entry, on the Pocket PC only, that
   fills the bag's Rare Candy stack to 999.
4. **The Pocket PC alone drops** the player's PC (items and mailbox), Oak's PC
   and the Hall of Fame viewer; the Pokemon Center PCs keep those three.
5. **Every PC drops** the Move Reminder (Pastoria's paid relearner is the only
   one), the Online Shop, the Teleport System, Happiness Up, every Move Tutor
   entry (the tutors out in the world stay as in vanilla) and all three
   post-game resets.
6. **The teleporting Abra** leaves every town. The base ROM has 39 objects
   using the Abra sprite, of three kinds, and Ian ruled on each (2026-09-27):
   the **22 town teleporters go** (the 18 with a destination list, and
   Canalave's, Twinleaf's, Route 221's at Pal Park and Route 224's); the **7
   dungeon shortcuts go** (Turnback Cave's pair, Stark Mountain's Heatran
   chamber, Mt. Coronet 6F and the two outside, and Route 207's list); the
   **10 gym shortcuts stay** (a pair in each of the Canalave, Pastoria,
   Snowpoint, Veilstone and Sunyshore gyms, entrance to leader and back).
   Each one that goes is hidden behind a flag set at new game, not deleted,
   since the generated scripts address objects by number.
7. **The Hidden Power APP** tells the power as well as the type: the IV
   formula, 30 to 70, which Ian kept.

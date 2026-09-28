# The Pocket PC: the base ROM's Vs. Seeker

Surveyed 2026-09-26 by the Carry-over Agent, from the base ROM's arm9 and its
`scripts_common`, so that Ian could rule on each function before any of it
moved. He ruled on all of it on 2026-09-27; the rulings are the last section,
and every one is built and merged: the item's hookup (488df5b9a), the trimmed
menus (4e6209dab), the Rare Candy entry (a09cb6669), the Hidden Power APP
(15b7995ba) and the Abra (894256fe2). Their in-game check is in
`docs/oxide/ingame-checklist.md`, section 3. The survey below describes the
base ROM, not Oxide.

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

`scripts_common` came over from the base ROM whole, so until the rulings were
built every Pokemon Center PC offered everything below, the free Move Reminder
included. The Pocket PC and the Pokemon Center PCs share that one menu: the
Pocket PC's entry sets `FLAG_POCKET_PC_OPEN`, the Pokemon Center's clears it,
and the entries only a Pokemon Center PC shows check it (4e6209dab).

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

Hooking the item up takes one thing away. **Vs. Seeker rematches end**, since the item
no longer runs the Vs. Seeker; nothing else in the game calls route trainers
back, and gym leaders return only through the reset above. In the base ROM
the teleporting Abra in each town is how a place is registered for the
Teleport System, and it teleports on its own too; ruling 6 below removes them.

## Rulings

Ian ruled on the whole list on 2026-09-27, relayed by the Overseer.

1. **Where it works:** everywhere, caves and buildings included, except in
   gauntlets: one-way areas the player must clear, beating a set number of
   trainers in a row, before leaving to heal. The mechanism is built
   (`MapHeader_IsGauntlet` in `src/map_header.c`), with no map marked yet; the
   tracker's "Gauntlets" entry says which areas are chosen.
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

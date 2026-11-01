# Argenta at Pal Park: her placement, and the bundle question

Ian placed Argenta, the Hall Matron, as an optional Frontier Brain in Pal Park lobby's north gallery on 2026-11-01, in Barry 5's stretch of Byron's split. This page covers that placement, built on the branch `overseer-argenta-place` the way Thorton's was, and puts her reward to Ian. Nothing here has been seen in game.

## Summary

Outcome. Argenta stands at the west end of the lobby's north gallery, facing east, once the Pal Park partner double is won. She appears the moment the double ends, without the player leaving the lobby, and on every later entry. She fights only when spoken to, and asks first. Her team is Ian's six at 50 in her trainer file, unchanged; only her trainer messages gave way to one defeat line, her Battle Hall line from the vanilla game. Her win gives a bundle of items once, under a spare flag; until it is given she offers it again when spoken to, and after it she has a closing line.

Ian's decision. Which bundle she gives. The script carries bundle A, below, until he answers.

| | Bundle | What it does for the player | Why |
|---|---|---|---|
| A, built | a Gold Bottle Cap and four Mints (Adamant, Modest, Jolly, Timid) | perfects one Pokemon: every IV to 31, and the nature its stats need | none of these is placed or sold anywhere yet (the tracker's open item of 2026-10-13); none is a held item, so no fight's item ceiling moves; it fits the Battle Hall, where one Pokemon faces every type. The four Mints are the natures most attackers want |
| B | Leftovers, Muscle Band, Black Sludge | three strong held items for fights | the Leftovers is otherwise only Victory Road's ball and Pickup, the Muscle Band only the post-game Battle Point exchange, the Black Sludge nowhere. Material: a Leftovers from Byron's split on reaches every later boss's box |
| C | a Gold Bottle Cap and three Bottle Caps | perfects one Pokemon's IVs, and one stat each of up to three more | spreads the gain across the box, as Ian's ruling that Bottle Caps be usable throughout suggests, and leaves the Mints for a later decision |
| D | Leftovers, a Gold Bottle Cap, a Jolly Mint and a Timid Mint | one strong held item, and one Pokemon perfected | the middle way between A and B; material through the Leftovers, as B is |

My recommendation is A. It is strong, it is the first home for items that have none, and it moves no fight's difficulty, so it needs no reading. B is the strongest for fights, and the one to take if Ian wants the reward felt in the next gym.

Left out on purpose: the Life Orb and the Choice items (never for the player), the Ability Patch (the one is Ace Trainer Jose's), the Lucky Egg (Ian dropped Route 207's on 2026-10-31), the Expert Belt and Focus Sash (Route 221's house gives them in turn, one a day, from this same split), the Wise Glasses and BlackGlasses (Celestic's house), PP Max (it would undo the expensive setup moves), and the element 7 held items, each of which already has its one optional trainer.

Difficulty: not material. Argenta is an optional fight whose team is unchanged, and bundle A holds no held item. Bundles B and D would be material from Byron's split on, through the Leftovers.

Next steps. Ian's answer on the bundle; a change to it is a few lines of her script and one line of her text ("They help one Pokemon become all it can be" fits A and C). Then Ian's in-game checks, about 15 minutes from a save that has won the Pal Park double (`ingame-checklist.md`, section 4, after Thorton's).

## How she is placed

| Part | Files | What |
|---|---|---|
| Her place | `events_pal_park_lobby.json` | a new object at (1, 5), the west end of the north gallery, which the player reaches up the lobby's east corridor; the four spectators stay where they were |
| Her gate | `scripts_pal_park_lobby.s` | while the lobby's state is below 2 (the double not yet won), the map's load sets `FLAG_MAP_LOCAL_0x01`, her hide flag; the game clears map-local flags on every map change, so this costs the save nothing. The double's last step clears it and adds her |
| Her fight | `scripts_pal_park_lobby.s`, `dummy_086.json` | she asks before the fight, as Dahlia, Darach and Thorton do, and "No" leaves her standing. An ordinary single battle; her defeat line is the vanilla Battle Hall's |
| Her bundle | `scripts_pal_park_lobby.s` | every item is checked for room before any is given, so the bundle arrives whole; then `FLAG_UNUSED_0x054D` is set. Each pocket holds one of every item in the game, so only a stack of 999 could refuse one |
| Her lines | `pal_park_lobby.json` | seven messages at the end of the bank, so every earlier id stays |
| Registers | `bulk_scripts.py`, `bulk_events.py`, `import_base_rom.py` | the lobby's script, events and text bank 515 already diverged for the double; each entry now names her too |

Her spare flag was chosen as Thorton's was: `FLAG_UNUSED_0x054D` is one of pret's unused flags in the reward placer's spare window, the next below the double's 0x054F and Thorton's 0x054E. Nothing names it in the tree, on `main`, or in the other helpers' branches, and the base ROM's scripts never use it (scanned by disassembly, and byte for byte in the 549 files that do not decode, with a known flag found as a control). It keeps its pret name, so the placer counts it as taken (`save-layout.md`).

She is not in `fights.json`. Thorton's entry there makes goal 3 read him as a story boss, which his commit marked material; adding her the same way is the Overseer's call.

## What could not be checked

Nothing was played. Her tile and the gallery's walking were read off the lobby's collision map. That a map-local flag hides an object until a script clears it is how vanilla's field-move obstacles work, but this is its first use on a person.

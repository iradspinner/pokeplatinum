# Signature moves

This answers Ian's request of 2026-10-20 on `unused-moves.md`: "lets do the moves pass for the last 3 categories in the list. Not every move needs to be necessarily placed, but we should at least see if they have a fitting home that improves a moveset or makes teambuilding more fun." It covers that page's last three picks (the signature moves that would suit obtainable lines, the trainer palette, the legendary signatures) and the other signature moves in its table of moves the engine runs as written. It was read from origin/oxide at 3ebc6bd576. Ian answered its first two questions the same day, and what he approved landed at 47d90c688: Stone Axe on Kleavor, learned on evolving; Lumina Crash on Slowbro and Slowking at 40; Baneful Bunker on Mareanie's egg list; and a fix to Judgment with the Pixie Plate. Shell Trap on Turtonator waits for in-game check 82 on `overseer-shell-trap-hold`.

## Summary

**Status (2026-10-21): Ian has answered every question below. Lumina Crash's home landed at 47d90c688. His answers to questions 3 to 6 landed at 67254f1d2, each applied row marked below: 41 level-up homes and 7 egg lists. Torch Song went to Magcargo at 63, his pick of the three candidates, landed at 8d633c9d0. The late-boss carriers wait until those teams are settled.**

**A correction first.** `unused-moves.md` named Glimmora as Lumina Crash's owner, and Ian approved it as a return on that basis. Lumina Crash is Espathra's (learned on evolving in Scarlet and Violet and in Legends Z-A). Oxide has no Flittle line, and no game gives the move to Glimmora. Ian's answer (2026-10-20): it goes to the Slowbro line at 40, the alternative below, and the Glimmora commit is dropped.

**Outcome.**

| Category | Moves read | Player homes | Trainer homes only | No home |
|---|---|---|---|---|
| Signature moves for obtainable lines: the 16 named, Lumina Crash, 35 more | 52 | 21 (Night Daze's post-game only) | 5, and 5 of the 21 also on a trainer-only list | 26 |
| Trainer palette | 5 | 0 | 5, on egg lists | 0 |
| Legendary signatures | 38 | 2, and Judgment post-game | 4 returns, 13 late-boss carriers | 15, and 3 settled before |

**The homes that matter most.**

| Home | Move, level | Why |
|---|---|---|
| Granbull | Spirit Break, 34 | A Fairy type with Attack 120 and no Fairy attack on its own list |
| Poliwrath | Jet Punch, 46 | No physical Water move at all |
| Galarian Rapidash | Spirit Break, 46 | Oxide's is Fairy and Fire, and every move of either type on its list is special |
| Kingdra, Seadra | Snipe Shot, 55 | With the Sniper and Focus Energy the line has, every Snipe Shot crits for 2.25 times; strong, so late |
| Cresselia | Esper Wing, 49 | Caught at 50 with no real STAB; this one speeds it up as it hits |
| Torterra | Drum Beating, 40 | The starter's physical Grass jumps from Razor Leaf (13) to Horn Leech (47); the Speed drop wants a close look |
| Duskull's egg list | Last Respects | Cyrus 2 and Cyrus 3 each carry a Dusknoir; sent in last, with five fainted, it hits for 300 |

**What Ian decides.**
1. Answered (Ian, 2026-10-20): Lumina Crash goes to Slowbro and Slowking at 40, not to Glimmora.
2. Answered (Ian, 2026-10-20): Shell Trap on Turtonator waits for in-game check 82, on its own branch, as Upper Hand and Burning Jealousy wait for 81 and 83.
3. Answered (Ian, 2026-10-21): the player homes go in as proposed, with four changes. Aqua Step goes to Golduck at 47. Torch Song does not go to Ninetales, a line too usable for it: it suits a slow Pokemon, or one of middling Sp. Atk, that would struggle to sweep with it. Ian picked its home from three candidates the same day ("Late game magcargo sounds good"): Magcargo at 63, kept late because Shell Smash (48) and Torch Song together are a sweep. Esper Wing goes to both Cresselia and Xatu, tentatively. Bitter Malice comes later than 46 on Spiritomb. The moves left without a home stay without one, the Pikachu moves among them.
4. Answered (Ian, 2026-10-21): the five egg lists go in as proposed.
5. Answered (Ian, 2026-10-21): the legendary returns go in as proposed. The late-boss carriers wait until those teams' compositions are settled (the tracker's Scheduled list): they gave Ian ideas, but the teams are not locked in.
6. Answered (Ian, 2026-10-21): in, all seven from Glitzy Glow to Sparkly Swirl, each on its own Eeveelution at a level in the last split or two (about 70 and up), since all are very strong. Sparkly Swirl's 85% is under the 90% bar for the player's moves; Ian's answer places it anyway.

**Difficulty.** The earliest player home is at 34, in Maylene's split, so none touches Roark or Gardenia. A player home is material for the fights whose boxes field its line at or above its level; a trainer home, for its boss. Applied, the homes reach goal 3's three boxes this way. Granbull's Spirit Break is in all three from Barry 3 and Maylene on, so every boss from Maylene's split to Cynthia is marked. Torterra's Drum Beating (box 1) and Dubwool's Raging Bull (box 3) come in at Barry 4 and Wake; Absol's Kowtow Cleave and Floette's Light of Ruin at Byron's split; Seadra's and Octillery's Snipe Shot at Candice's; Cresselia's Esper Wing at Volkner; Glaceon's Freezy Frost and Sylveon's Sparkly Swirl at Barry 6 and the League; Cresselia's Lunar Blessing in the League; Magcargo's Torch Song (box 1) at Somnu 2 and the four fights at 65 in Cyrus 3's split, and every boss after. Every box keeps its Floette unevolved, since the boxes take no stone evolutions, so all three field Light of Ruin from 50, not only a Floette held back. No box fields the other lines at their levels, and the egg lists and trainer homes change no team.

**Next steps and time.**
- The approved homes and egg lists: landed at 67254f1d2 (2026-10-21).
- Torch Song on Magcargo at 63: landed at 8d633c9d0 (2026-10-21).
- Each team change Ian takes: that boss's question, then its reading, 1 to 2 hours of machine time.
- Every move on this page now runs in the readings (below).

## How the homes were chosen

Obtainability is `pool.obtainable()`, the first catches are `pool.caught()`, and evolution items come from `pool.evolution_items_first()` (Moon Stone and Leaf Stone from Gardenia's split, Fire and Water Stones from Maylene's, the Shiny Stone from Wake's). The ladder is the learnset generator's (`learnrewrite.climbs` and `within_ceiling`), read against today's lists at the earliest split a player has the stage at that level. "Climbs" means the generator's own check passes. "A rung over" or "jumps" means it does not, and the table says why the gap is worth it. "By hand" marks a move the generator cannot place: a first move of its kind on that side, a line with no catch in the main run, or a move it holds off.

Every move in the first two parts below belongs, in the later games, to a species Oxide lacks or the player cannot obtain; only three of the legendary returns (Lunar Blessing, Light of Ruin and Judgment) go to an owner the player can have. hg-engine's per-game lists (Black and White to Legends Z-A) give the owner and its level; the home in Oxide comes from type, stats, ability, role, the gap in the line's list, and the move's theme. Levels were picked free on each list, so no two moves share one.

The rules that bite: speed control and priority are strong, so those moves come after Wake's split on lines that are not already fast; the player's moves meet R37's 90% bar; no weather for the player; Protect variants stay off player lists; one two-to-five-hit move per type; a sure status on a hit is Thunder Wave's or Will-O-Wisp's reliability, which the player gets only as a single TM; and a move meant only for trainers never lands in a wild catch's four.

Oxide's critical hits follow Generation 7: one stage is 1 in 8, two stages 1 in 2, three every hit, at 1.5 times, and a Sniper's at 2.25 times (`BattleSystem_CalcCriticalMulti`). Snipe Shot and Esper Wing are read with that.

## Engine and simulator notes

The engine runs every move on this page as written, as `unused-moves.md` found.

The readings now run every move on this page as the engine does (checked on 2026-10-21 against `simulator-gaps.md` at 8c28ec9f34). When the page was written they did not run these effects, and batches 13 and 14 fixed each, all on oxide:

| Move | What the readings did instead | Fixed at |
|---|---|---|
| Stone Axe, Ceaseless Edge | a plain hit: no rocks, no Spikes | f84a899e3 |
| Dire Claw | a plain hit: no status | 73529138a |
| Esper Wing | the critical stage ran; the Speed rise did not | 953087fd4 |
| Glitzy Glow, Baddy Bad, Freezy Frost, Sappy Seed, Sparkly Swirl | plain hits: no screen, no reset, no seed, no cure | 8538b5e4d, c8d9db11e, 394996e0e, 31b5205ff |
| Lunar Blessing, Jungle Healing | nothing happened | adf13d1bb |
| V-create | a plain 180 hit; the user's stats never fell | 3bdba0c6d |
| WildboltStorm, BleakwindStorm, SandsearStorm | plain hits at 80% whatever the weather | e8b0585e1, afae81daf, e199d382e, the rain's sure hit at 99fc746a8 |
| Freeze Shock, Ice Burn | ran wrongly | 0f37af551 |
| Hyperspace Fury | through Protect, but the user's Defense never fell | 35dd11723 |
| Judgment, Surging Strikes | approximately | 9d0b6b7b3 (the player's Plates at 0ce5ec6e2), 17d72e842 |
| Last Respects | held at 50: the engine adds 50 to its power for each fainted member of the user's party (`BattleScript_ComputedMovePower`), which fightsim's `STATE_POWER_MOVES` lacked. This page found it; Ian added it to the gaps on 2026-10-20 | e1a1c7c06 |

The late bosses' table at the end keeps its Simulator column as it was on 2026-10-20, since Ian holds that table until those teams are settled.

Shell Trap has worked in the engine since 2026-10-07, and the readings run it, but in-game check 82 is still open, and `learncheck.UNCHECKED` still lists it, so learncheck's check 16 would report the Turtonator entry as "not run as designed" (it fails no test). Ian held the entry for the check (2026-10-20); it waits on `overseer-shell-trap-hold`, in the tracker's Scheduled list.

## The signature moves with homes

"For" says whether a home serves the player or only trainers. A trainer home on the list of a species the player cannot obtain makes the move legal for trainers and changes no team; from Cyrus 3's split on, a trainer's move need not be legal at all. "Applied" marks a home written on `overseer-signature-moves-3` from Ian's answers of 2026-10-21 and landed at 67254f1d2; the trainer homes beside the player homes went in with them.

### Fairy

#### Spirit Break
Physical, 75, 100%, 15 PP; lowers the target's Sp. Atk a stage every hit. Grimmsnarl's, learned on evolving, from Sword and Shield on. The simulator runs it (fixed at 84f2868a3).

| Home | Level | Ladder | What it changes | For |
|---|---|---|---|---|
| Granbull | 34, Maylene | climbs: the foot of the physical Fairy ladder | Applied. Granbull's own list has no Fairy attack; Snubbull's Dazzling Gleam (17) is special, off its Sp. Atk of 60. Intimidate and a Sp. Atk drop on every hit make it a wall against both kinds of attacker. Flagged by Attack, so after Fantina's split. Maylene's Fighting types meet it, so it is material for Maylene; 40 would leave her fight as it is | player |
| Galarian Rapidash | 46, Byron | climbs | Applied. Oxide's Galarian Rapidash is Fairy and Fire with Attack 105, and every Fairy and Fire move on its list is special. A Moon Stone makes one from a Ponyta in Gardenia's split, so this flagged line (Attack 105, Speed 110) waits until Byron's | player |

### Water

#### Snipe Shot
Special, 85, 100%, 15 PP; a high critical-hit ratio. Inteleon's, learned on evolving, from Sword and Shield on. The simulator runs it.

| Home | Level | Ladder | What it changes | For |
|---|---|---|---|---|
| Seadra, Kingdra | 55, Candice | climbs from Octazooka (85) | Applied. The Horsea line has Sniper in its second slot and Focus Energy (3 PP) at 14, and its Water moves stop at Octazooka (40). After one Focus Energy, every Snipe Shot is a critical hit at 2.25 times, past the target's Sp. Def rises and Light Screen: it lands like a 190-power move. That is why it fits, and why it waits for Candice's split. A Scope Lens, sold at the Fight Area, gives the same with any move, later | player |
| Octillery | 56, Candice | climbs from Scald (80) | Applied. Remoraid is the Pokedex's sharpshooter, and Octillery has Sniper in its second slot and Focus Energy at 23. Its Water moves stop at Scald (35). The same combination, on a flagged line | player |

#### Jet Punch
Physical, 60, 100%, 15 PP, priority +1; a punch. Palafin's, at 1. The simulator runs it.

| Home | Level | Ladder | What it changes | For |
|---|---|---|---|---|
| Poliwrath | 46, Byron | climbs | Applied. Poliwrath's only Water move is BubbleBeam at 1, special; it has no physical Water move at all. The punching line gets a Water punch with priority, a rung over Aqua Jet (40), the type's other priority move. With Victory Dance at 50 it becomes a priority sweeper, so it comes after Wake's split | player |

#### Aqua Step
Physical, 80, 100%, 10 PP; raises the user's Speed a stage every hit; a dance. Quaquaval's, learned on evolving. The simulator runs it (fixed at 23833a1aa).

| Home | Level | Ladder | What it changes | For |
|---|---|---|---|---|
| Golduck | 47, Byron | climbs | Applied: Ian took this one (2026-10-21). The duck's move on the duck. Golduck is mixed (Attack 82, Sp. Atk 95), and its physical Water moves are Aqua Jet (1) and Flip Turn (68). One hit raises its Speed 85 by half, past most foes of base Speed 120. Speed control, so after Wake's split | player |
| Feraligatr | 46, Byron | climbs | Not applied: Ian took Golduck (2026-10-21). Feraligatr's only physical Water move is Aqua Tail at 58 (Croconaw's at 48). On Attack 125 a Speed rise every hit comes close to a Dragon Dance each turn: the bigger change, on a flagged line | player |

### Dark

#### Night Daze
Special, 90, 100%, 10 PP; lowers the target's accuracy 30% of the time. Zoroark's (64 in Black and White; Zorua's 40 in Scarlet and Violet). The simulator runs it.

| Home | Level | Ladder | What it changes | For |
|---|---|---|---|---|
| Darkrai | 47 | by hand: no main-run catch | Applied. The Pitch-Black Pokemon has no special Dark move on its list (Faint Attack 29, Dark Void 66). It serves the post-game Darkrai, and Officer Somnu's Darkrai (63) could carry it legally; his fight is a question for Ian | player (post-game); Somnu |

No main-run home: the lines that lack a special Dark move (Absol, Sharpedo) are physical first, and the special ones already have Dark Pulse.

#### Kowtow Cleave
Physical, 85, never misses, 10 PP; a slicing move. Kingambit's, learned on evolving. Oxide has no Pawniard line. The simulator runs it.

| Home | Level | Ladder | What it changes | For |
|---|---|---|---|---|
| Absol | 50, Byron | two rungs over: a flagged Absol may climb to 75 from Sucker Punch (70) | Applied. Absol's Dark moves are Pursuit (20), Bite (28), Sucker Punch (44, 5 PP) and Night Slash (52): no accurate 80 or more. A blade horn for a slicing move, and never missing answers the accuracy drops and evasion it meets | player |

### Grass

#### Apple Acid
Special, 90, 100%, 10 PP; lowers the target's Sp. Def a stage every hit. Appletun's, at 28. The simulator runs it.

| Home | Level | Ladder | What it changes | For |
|---|---|---|---|---|
| Tropius | 46, Byron | a rung over: from Leaf Tornado (65) the ladder allows 80 | Applied. The fruit Pokemon. Its special Grass runs Leaf Tornado (26) and Magical Leaf (31), then SolarBeam (51), which needs the sun the player never sets, and Leaf Storm (61). This is its real Grass move. At 46 it comes after Wake, whose Water team it would hit; 42 would make it material for Wake | player |
| Exeggutor | 42 | trainers | Applied. Not obtainable. On its list a later trainer's Exeggutor carries it legally; Gardenia's Exeggutor (24) is untouched | trainer |

#### Grav Apple
Physical, 90, 100%, 10 PP; lowers the target's Defense a stage every hit, and half as strong again under Gravity. Flapple's, at 32. The simulator runs it, the Gravity boost included.

| Home | Level | Ladder | What it changes | For |
|---|---|---|---|---|
| Shiftry | 50, Byron | climbs, after Leaf Storm (49) | Applied. Attack (100) is Shiftry's better stat, but a Leaf Stone Shiftry's own list has no physical Grass move beyond Razor Leaf at 1. Seedot hangs from a branch until it is heavy enough to drop with a thump, which is the move's whole idea | player |

#### Drum Beating
Physical, 80, 100%, 10 PP; lowers the target's Speed a stage every hit. Rillaboom's, learned on evolving. The simulator runs it.

| Home | Level | Ladder | What it changes | For |
|---|---|---|---|---|
| Torterra | 40, Wake | climbs | Applied. The Grass starter that carries a tree: Torterra's physical Grass runs from Razor Leaf (13) to Horn Leech (47). A sure Speed drop lets a Speed 56 tank move first from the second turn against the foes that outpace it now. It comes after Maylene's split. Turtwig is the starter of one goal 3 box in three, so this is material for every fight from Wake's split that those boxes read | player |

### Fire

#### Torch Song
Special, 80, 100%, 10 PP; raises the user's Sp. Atk a stage every hit. Skeledirge's, learned on evolving. The simulator runs it.

| Home | Level | Ladder | What it changes | For |
|---|---|---|---|---|
| Ninetales | 48, Byron | climbs | Not applied: Ian, 2026-10-21, finds Ninetales a line too usable for it. A Fire Stone Ninetales's own special Fire is Ember (1), then nothing until Mystical Fire (62); only a Vulpix evolved after 24 keeps Flamethrower. A wild Ninetales caught at 50 would know it. Fiery Dance (a boost half the time) and Mystical Power (a Psychic move at 90%) were approved with the same kind of boost on 2026-10-14; this one boosts on every hit and never misses, so on a flagged line it waits until Byron's split. Flint's Ninetales could carry it too | player |

Ian's answer (2026-10-21): Torch Song suits a slow Pokemon, or one of middling Sp. Atk, that would struggle to sweep with it. He picked Magcargo the same day, late in the game ("Late game magcargo sounds good"), so the move is applied at 63, not the 50 proposed below. 63 is free on its list, in the Galactic split, after Flamethrower (61) and before Energy Ball (64), and the generator reads it as a climb; it keeps the Shell Smash sweep out of Byron's, Candice's and HQ's splits. Turtonator and Flareon get nothing. Speed and Sp. Atk are Oxide's base stats; "climbs" is the generator's own ladder check at that level and split.

| Candidate | Speed | Sp. Atk | First had | Level | On the special Fire ladder |
|---|---|---|---|---|---|
| Magcargo | 30 | 109 | as Slugma, wild on Route 210 at 21 in Maylene's split; it evolves at 30 | Applied at 63, Galactic (proposed 50, Byron) | climbs: the rung of its Lava Plume (80, at 40), below Flamethrower (90, at 61) |
| Turtonator | 36 | 91 | wild on Route 211 at 28, in Byron's split | 48, Byron | climbs: a rung under its Flamethrower (90, at 38), ten points of power traded for a boost every hit |
| Flareon | 65 | 95 (Attack 130) | Eevee at 20, with a Fire Stone from Maylene's split | 46, Byron | climbs: its first special Fire move after Fire Spin (36) and before Heat Wave (71), off its better stat |

Magcargo and Turtonator are the slowest Fire types the player can have. Each already learns Shell Smash (Magcargo at 48, Turtonator at 45), which doubles its Speed, so on either Torch Song makes a slow setup line, frail after the Shell Smash; Magcargo also keeps its double weaknesses to Water and Ground. Flareon is the mildest choice: a physical attacker (Fire Lash at 50, Sizzly Slide at 70) whose Sp. Atk would build from 95 on a Speed of 65. Torkoal (Speed 20, Sp. Atk 85) and Camerupt (40, 105) fit the test best but are not obtainable in Oxide, so a home there would serve trainers only. Every other obtainable Fire line ends fast or far above middling Sp. Atk (Chandelure, Volcarona, Delphox, Houndoom, Magmortar, Charizard, Blaziken, Armarouge, Salazzle).

### Psychic

#### Lumina Crash
Special, 80, 100%, 10 PP; lowers the target's Sp. Def two stages every hit. Espathra's, learned on evolving (Scarlet and Violet, Legends Z-A). The simulator runs it (fixed at 5250b68bf).

| Home | Level | Ladder | What it changes | For |
|---|---|---|---|---|
| Glimmora | 46, Byron | climbs from Wake's split on | Not applied: Ian took the Slowbro line instead (2026-10-20). A special attacker (Sp. Atk 130) that already has Acid Spray's two-stage drop at 7: it adds power and Psychic coverage, against the Fighting and Poison types that resist one of its types, to a role Glimmora has. The light of its crystal petals fits the move | player |
| Slowbro, Slowking | 40, Wake | climbs on Slowbro; a rung over on Slowking | Applied on `overseer-signature-moves-2` (Ian, 2026-10-20). The Slowpoke line's special Psychic runs from Confusion (15) to Psychic (48 on Slowking, 54 on Slowbro), one of the longest gaps among Oxide's special Psychic lines | player |

#### Esper Wing
Special, 80, 100%, 10 PP; a high critical-hit ratio, and raises the user's Speed a stage every hit. Hisuian Braviary's (25 in Legends: Arceus; on evolving in Scarlet and Violet). The simulator runs it (the Speed rise fixed at 953087fd4).

| Home | Level | Ladder | What it changes | For |
|---|---|---|---|---|
| Cresselia | 49, Volkner | climbs | Applied, tentatively, beside Xatu's (Ian, 2026-10-21). Met at 50 from Acuity Cavern's draw (one run in three), Cresselia's special Psychic moves are Confusion (1) and Future Sight (38), and it is caught knowing Mist, Aurora Beam, Future Sight and Slash. At 49 the catch knows Esper Wing in Mist's place: a STAB that speeds a slow-building wall up as it hits, beside Take Heart (54). One hit raises its Speed 85 by half, past most foes of base Speed 120 | player |
| Xatu | 50 | trainers | Applied, tentatively. Not obtainable; the Psychic and Flying bird is the nearest owner Oxide has | trainer |

#### Psyshield Bash
Physical, 90, 90%, 10 PP; raises the user's Defense a stage every hit. Wyrdeer's, and Stantler's at 21 in Legends: Arceus, an egg move in Scarlet and Violet. The simulator runs it.

| Home | Level | Ladder | What it changes | For |
|---|---|---|---|---|
| Solrock | 44, Byron | by hand: its first physical Psychic move | Applied. Attack (110) is Solrock's better stat, but its Psychic moves, Confusion and Psybeam, are special. A Defense rise on every hit suits a bulky Rock type (HP 90, Defense 95). Its 90% meets R37. Met in Byron's split at 31 | player |
| Stantler's egg list | | trainers | Applied. Not obtainable; its own move in the later games. Officer Somnu's Stantler (62) could take it, as a question | trainer |

### Ghost

#### Bitter Malice
Special, 75, 100%, 10 PP; lowers the target's Attack a stage every hit. Hisuian Zorua's and Zoroark's (40 and 46 in Scarlet and Violet). The simulator runs it.

| Home | Level | Ladder | What it changes | For |
|---|---|---|---|---|
| Spiritomb | 54, Candice (proposed 46, Byron) | climbs from Hex (42) | Applied at 54: Ian asked for it later than 46 (2026-10-21). At 46 it came three levels before Dark Pulse (49), so both of a strong line's STAB moves climbed inside Byron's split; at 54, the first level of Candice's split and free on its list, each type climbs in its own split: Hex in Wake's, Dark Pulse in Byron's, Bitter Malice in Candice's. Spiritomb's special Ghost moves are Ominous Wind (25) and Hex (42), with no Shadow Ball. A hundred and eight spirits bound by resentment, and an Attack drop that suits a slow wall with 108 in each attacking and defending stat, caught at 25 | player |
| Mismagius | 46, Byron | climbs from Hex (40) | Applied. A Dusk Stone Mismagius's own Ghost moves are Ominous Wind (17) and Hex (40); only a Misdreavus kept to 37 learns Shadow Ball. A witch's curse on a fast, flagged attacker | player |

#### Infernal Parade
Special, 65, 100%, 15 PP; burns 30% of the time, and doubles against a target with a status. Hisuian Typhlosion's (40 in Legends: Arceus). The simulator runs it.

| Home | Level | Ladder | What it changes | For |
|---|---|---|---|---|
| Litwick, Lampent, Chandelure | 38, Maylene | climbs from Hex | Applied. Ghost and Fire, Hisuian Typhlosion's types. Their Ghost moves run from Hex (30) to Shadow Ball (55, 56 or 65). A Hex that makes its own burn: 65 with a 30% burn against a healthy foe, 130 against a burned one. It adds no power over Hex after Will-O-Wisp (22), so it is a small change even on a flagged Chandelure | player |
| Typhlosion | 48 | trainers | Applied. Not obtainable; its Hisuian form's move | trainer |

### Electric

#### Thunderclap
Special, 70, 100%, 5 PP, priority +1; fails unless the target is about to attack (Sucker Punch's rule). Raging Bolt's, at 49. The simulator runs it.

| Home | Level | Ladder | What it changes | For |
|---|---|---|---|---|
| Ampharos | 52, Byron | climbs | Applied. Oxide's Ampharos is Electric and Dragon, Raging Bolt's types, slow (Speed 55) with Sp. Atk 115. A priority STAB lets it strike before the faster foes that attack it, and 5 PP keeps it a finisher. Priority is part of planning on both sides (Ian, 2026-10-06); flagged, so at the end of Byron's split | player |

### Normal

#### Raging Bull
Physical, 90, 100%, 10 PP; breaks Reflect and Light Screen before it hits. Paldean Tauros's; Tauros learns it at 35 in Scarlet and Violet. The simulator runs it (fixed at 74899d5eb).

| Home | Level | Ladder | What it changes | For |
|---|---|---|---|---|
| Dubwool | 42, Wake | climbs | Applied. The ram's charge: a 90 without the recoil of Take Down (27) or Double-Edge (50), and a screen breaker for Byron's, Lucian's and Saturn's screens | player |
| Tauros | 36 | trainers | Applied. In Oxide but not obtainable; its Scarlet and Violet level is 35, which Take Down holds | trainer |

### More signature moves from the table

These are the other signature moves in `unused-moves.md`'s table of moves that run as written whose home is plain. Eevee's and Pikachu's partner moves come from Let's Go; Ian may take them as a set or leave them. Ian took Eevee's seven (2026-10-21: "they're all insanely good"), each on its own Eeveelution in the last split or two, and left Pikachu's out. Each is at 70, free on all seven lists and a level before the 71 that five of them already learn, so Barry 6 and the League's five fights field them; Ian watches Sizzly Slide and Buzzy Buzz in those readings. The proposed homes are in brackets.

| Move | Oxide's numbers | Home | Why | Simulator |
|---|---|---|---|---|
| Glitzy Glow | Psychic, special 80, 95%; Light Screen on a hit | Applied: Espeon 70, climbs (Espeon 44) | after Psychic (64), a screen on every hit | runs |
| Baddy Bad | Dark, special 80, 95%; Reflect on a hit | Applied: Umbreon 70, climbs (Umbreon 50) | off its Sp. Atk of 60, but a screen on every hit suits a support Umbreon | runs |
| Freezy Frost | Ice, special 100, 90%; resets every stage on a hit | Applied: Glaceon 70, a jump from Freeze-Dry's 70 power (Glaceon 64) | Haze on an Ice Beam, an answer to a boss's setup, a level before Ice Beam (71) | runs |
| Sappy Seed | Grass, physical 100, 90%; Leech Seed on a hit | Applied: Leafeon 70, a jump from Horn Leech's 75 (Leafeon 66) | a late hit that plants Leech Seed, a level before Leaf Blade (71) | runs |
| Sizzly Slide | Fire, physical 60, 100%; a sure burn on a hit | Applied: Flareon 70, climbs (Eevee's egg list) | Will-O-Wisp's reliability on a hit, which the player otherwise gets only from a single TM | runs |
| Buzzy Buzz | Electric, special 60, 100%; a sure paralysis on a hit | Applied: Jolteon 70, climbs (Eevee's egg list) | Thunder Wave's reliability on a hit, likewise | runs |
| Sparkly Swirl | Fairy, special 120, 85%; cures the party's status | Applied: Sylveon 70, a jump from Moonblast (43) (Eevee's egg list) | under R37's 90% bar, which Ian's answer sets aside; `learncheck.R37_EXCEPTIONS` records it beside Pelipper's Hurricane | runs |
| Raging Fury | Fire, physical 120, a third as recoil, 20% confusion | Applied: Infernape 65 (its Scarlet and Violet level) and Growlithe's egg list | Hisuian Arcanine's; neither line is obtainable, and the player has Flare Blitz on many lines | runs |
| Shadow Bone | Ghost, physical 85, 20% Defense drop | Applied: Marowak 28 (27, its later games' level, holds False Swipe) | Alolan Marowak's; Marowak is in Oxide but not obtainable | runs |

### Moves left without a home

| Move | Reason |
|---|---|
| Veevee Volley, Pika Papow | power by friendship and never miss: Return and Frustration already serve |
| Zippy Zap | raises the user's evasion on every use: Ian took Double Team off every player list, and evasion setups are rare for trainers. The readings ran it wrongly when this was written (fixed since at 09f607e70) |
| Floaty Fall, Splishy Splash | Pikachu's partner coverage; nothing in Pikachu's or Raichu's lists asks for Flying or Water |
| Silk Trap, King's Shield, Spiky Shield, Obstruct, Burning Bulwark | Protect variants, off player lists; their owners are not in Oxide, and trainers already have Protect and Detect |
| Steamroller, Gear Grind, Spin Out, Overdrive, Order Up, Syrup Bomb, Spicy Extract | owners Oxide lacks and no line that asks for them. Order Up's effect needs a Tatsugiri inside its user; the readings did not run Spin Out's or Spicy Extract's effects when this was written (fixed since at b346795eb and 5bd5d24a0) |
| Fickle Beam, Bolt Beak, Fishious Rend | the readings ran them approximately or wrongly when this was written (Bolt Beak and Fishious Rend always doubled; fixed since at 12753f216 and da8c63505), and Ian's answer 3 keeps them without a home |
| Electro Shot | a charge move that skips its charge in rain, which the player never sets |
| Population Bomb | one two-to-five-hit move per type: Normal keeps Fury Swipes and Tail Slap. The readings ran it wrongly when this was written (fixed since at 80c2e60bb) |
| Mountain Gale | 85% (R37), and Oxide has no Bergmite line |
| Head Charge | Double-Edge is the same 120 with the same recoil |
| Chloroblast | half the user's HP: half a forced trade, as Mind Blown is. The readings took no HP when this was written (fixed since at 051820a6c) |
| Meteor Assault | a recharge turn |

Eerie Spell and Burning Bulwark, which the stranded-moves pass left without a home, are not signature moves; the Slowpoke line's Psychic gap (above, under Lumina Crash) would suit Eerie Spell too.

## The trainer palette

Each goes on the egg list of a line's first stage, which trainers may use and the player never reaches. All five are applied (Ian, 2026-10-21), each held in `learnrewrite.IAN_EGG_MOVES` so that a generator run keeps it; no trainer carries one yet.

| Move | Oxide's numbers | Egg list | Why there | Simulator |
|---|---|---|---|---|
| Ceaseless Edge | Dark, physical 65, 90%; a layer of Spikes on a hit; slicing | Applied: Corphish (Crawdaunt) | Hisuian Samurott's. Crawdaunt is Water and Dark, its types, and slices with its claws | runs |
| Dire Claw | Poison, physical 80, 100%; poisons, paralyses or puts to sleep 30% of the time | Applied: Sneasel (Weavile) | Sneasler's, which a Hisuian Sneasel becomes. Cyrus 2's Weavile is the trainer it fits | runs |
| Barb Barrage | Poison, physical 60, 100%; poisons half the time, doubles against a poisoned target | Applied: Qwilfish | Overqwil's; Qwilfish has it as an egg move in Scarlet and Violet. Legends Z-A gives it by level at 28, which would fill Qwilfish's own physical Poison gap (Poison Sting at 1 to Poison Jab at 49) if Ian wants it for the player | runs |
| Malignant Chain | Poison, special 100, 100%; badly poisons half the time | Applied: Gastly (Gengar) | Pecharunt's, which is Poison and Ghost, Gengar's types | runs |
| Last Respects | Ghost, physical 50, and 50 more for each fainted member of the user's party | Applied: Duskull (Dusknoir) | Houndstone's. Dusknoir guides spirits; Cyrus 2 and Cyrus 3 each carry one, and as the last member with five fainted it hits for 300. Material for any fight that takes it | runs |

## Legendary signatures

### Back to an owner Oxide has

All seven are applied (Ian, 2026-10-21).

| Move | Owner | Level | Who can have it | Simulator |
|---|---|---|---|---|
| Lunar Blessing | Cresselia | 72, its Scarlet and Violet level | The player, from Acuity Cavern's draw. Heals a quarter and cures status; in a single battle it is a weaker Moonlight (57) with Take Heart's cure | runs |
| Light of Ruin | Floette | 50, where X and Y to Ultra Sun and Moon give it to Floette | The player: Floette is the Day Care gift at 30 in Maylene's split. Fairy, special 140, 100%, half the damage as recoil. A Floette held back from its Shiny Stone to 50 learns it, and keeps it as a Florges: the Eternal Floette never evolved either. The generator reads it as a jump, over the ceiling in Byron's split; the recoil is the price. Florges at 68, inside the ceiling though still a jump, is the other choice. Goal 3's boxes take no stone evolutions, so every box keeps its Floette and fields Light of Ruin from 50 | runs |
| Judgment | Arceus | 75 | The post-game Arceus. Its type follows a held plate: until the fix on `overseer-signature-moves-2` (Ian, 2026-10-20), the Pixie Plate's Judgment hit as Normal | runs |
| Psystrike | Mewtwo | 72, its Sword and Shield level | trainers only | runs |
| Precipice Blades | Groudon | 63, its Sword and Shield level (Oxide's 45 holds Lava Plume) | trainers only | runs |
| Dragon Ascent | Rayquaza | 1, as from Sword and Shield on | trainers only | runs |
| Fleur Cannon | Magearna | 49, its Sun and Moon level | trainers only (Magearna sits in Valor Cavern's third, drawn nowhere) | runs |

Mind Blown (Blacephalon), Geomancy (Xerneas) and Land's Wrath (Zygarde) are on their owners already, and the stranded-moves pass settled them on 2026-10-14.

### For the late bosses

From Cyrus 3's split on a trainer's move need not be legal. Each row is one carrier that fits; Cynthia appears four times so that Ian can pick, not so that she takes all four.

| Move | Oxide's numbers | A late boss that could carry it | Simulator |
|---|---|---|---|
| V-create | Fire, physical 180, 95%; the user's Defense, Sp. Def and Speed fall | Flint's Infernape | does not run (no drops) |
| Searing Shot | Fire, special 100, both foes and the partner; 30% burn | Flint's Magmortar | runs |
| Blue Flare | Fire, special 130, 90%; 20% burn | Cyrus 3's Heatran | runs |
| Bolt Strike | Electric, special 130 in Oxide, 90%; 20% paralysis | Volkner's Jolteon | runs |
| Steam Eruption | Water, special 110, 100%; 30% burn | Cynthia's Milotic, in place of Scald | runs |
| Hyperspace Fury | Dark, physical 100, never misses, through Protect; the user's Defense falls | Aaron's Drapion | the Defense drop does not run |
| Hyperspace Hole | Psychic, special 80, never misses, through Protect | Lucian's Alakazam | runs |
| WildboltStorm, BleakwindStorm | Electric and Flying, special 100, 80%, sure in rain | a late rain team's Zapdos or Pelipper | do not run |
| SandsearStorm | Ground, special 100, 80%; 20% burn | Bertha's Nidoking | does not run |
| SpringtideStorm | Fairy, special 100, 80%; 30% Attack drop | Cynthia's Togekiss | runs |
| Astral Barrage | Ghost, special 110, both foes | Cynthia's Spiritomb | runs |
| Secret Sword | Fighting, special 85, against Defense | Cynthia's Lucario | runs |

Left without a carrier: Eternabeam and Prismatic Laser (a recharge turn); Dynamax Cannon, Dragon Energy, Tera Starstorm, Behemoth Blade and Behemoth Bash (plain hits the late teams' own moves cover, and the late Dragons are physical); Freeze Shock and Ice Burn (a charge turn, and no late Ice boss); Glacial Lance (no late physical Ice); Double Iron Bash (on Aaron's Technician Scizor it would land 90 twice); Wicked Blow and Surging Strikes (always critical, which a Sniper would make 2.25 times); Ruination (Nature's Madness and Super Fang do it); Jungle Healing (Lunar Blessing's twin).

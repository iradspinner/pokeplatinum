# The early kits on the type ladders: a player's read

Written 2026-10-06 on the branch `balance-tm-pass`, for Ian to spot-check.
It reads every line's first split, catch and level-up alike, on the lists
the type ladders build, against the lists that landed with the learnset
rewrite.

## Summary

**Outcome.** The generator no longer fills a gap with the strongest move a
power ceiling lets through. Each type's attacks form a ladder by power,
physical and special side by side, and a line climbs its side: its first
move of a type comes from the low rungs at the point in the game, and it
climbs one or two rungs a split (one for a power-flagged line, one fewer in
the split it is caught in). A move is read halfway between its power and
the power the line feels through its own attacking stat, so an off-stat
move sits lower. The ceilings stay only as a cost in the score. The early
Giga Drains are gone, and BubbleBeam stays on Corphish at its own level.

| Check | Landed | Ladders |
|---|---|---|
| 7, R1: five moves in the first split (203 lines) | 4 | 6 |
| 8, R2: two new moves per eight levels held (454 stages) | 117 | 160 |
| 9, R4: coverage by the second split (203) | 1 | 1 |
| 10, R5: three coverage types over the game (226) | 4 | 4 |
| 14, R11: an attack of each type within a split (454) | 0 | 0 |
| 23, R16: a newer move on every line (203) | 1 | 1 |
| 24: branches within 80% of each other (16) | 0 | 2 |

The ladders cost R2 most: a band that asks for two new moves finds fewer
that fit when a line may only climb, and the generator leaves it short
rather than add filler. The two branch choices that read apart are Eevee's
and Wooper's.

**Ian's action item.** Spot-check the list below: each strong early attack
the ladders put where the landed lists did not, one line each. Strike any
that reads wrong; the generator's rule changes, not the one line.

## The cases Ian named

| Line | Landed | Ladders |
|---|---|---|
| Seedot (caught 4) | Giga Drain at 4 | Mega Drain at 4, no Grass attack above 40 in Roark's split |
| Hoppip (caught 12) | Giga Drain at 12 | Mega Drain at 12, Magical Leaf at 13; Giga Drain at 37 |
| Treecko (caught 9) | Giga Drain at 9 | Magical Leaf at 8 and Mega Drain at 9; Giga Drain at 46 |
| Corphish (caught 3) | BubbleBeam at 3 | BubbleBeam at 20, Oxide's own level |
| Zubat (caught 3) | Venoshock and Wing Attack at 3 | Poison Sting at 3, Peck at 7; Wing Attack at 17 |
| Chinchou (caught 3) | Spark at 3 | ThunderShock at 3, Spark at 20 |
| Nidoran♀ (caught 4) | Sludge at 4 | Mud Shot at 3, Clear Smog at 6 |

## Strong early attacks to spot-check

Every attack of 60 power or more a line knows at capture or learns in its
first split that the landed lists did not give it there. Each is a first
rung or a one-rung climb on its type's ladder; most are 60, the foot of a
sparse side.

- Tentacool, Remoraid, Psyduck, Squirtle (caught 3 to 4) and Feebas and Popplio (Gardenia's split): Flip Turn 60 at capture, a pivot as the first physical Water rung.
- Corsola: Flip Turn 60 at 10, the same.
- Lotad: Magical Leaf 60 at 5, the second special Grass rung after Mega Drain.
- Hoppip: Magical Leaf 60 at 13, the same.
- Treecko: Magical Leaf 60 at 8, the first special Grass rung at Gardenia's starting point.
- Treecko: DragonBreath 60 at 13, its Dragon coverage at the line's level.
- Murkrow: Ominous Wind 60 at 10, Ghost coverage at its level.
- Fennekin: Incinerate 60 at capture (8), its first special Fire rung.
- Rhyhorn: Bite 60 at 13, Dark coverage at the level of its Horn Attack.
- Gligar: Bulldoze 60 at capture (8), the first physical Ground rung.
- Onix: Bite 60 at capture (5), Dark coverage at the level of its Bulldoze.
- Pawmi: Spark 65 at 5, the first physical Electric rung (the side has no 40 to 60).
- Pawmi: Bite 60 at 8, Dark coverage at Spark's level.
- Wooloo: Round 60 at 6, a Normal climb from Tackle.
- Squirtle: Flip Turn 60 at capture (3), above.
- Snivy: Breaking Swipe 60 at 8, Dragon coverage that lowers Attack.
- Charmander: Bite 60 at 10, Dark coverage at Flame Wheel's level.
- Hoothoot: Aerial Ace 60 at 20, a climb from Peck in Gardenia's split.

The full list of every line whose first-split attacks changed is in the
generator's log (`tools/oxide/balance/learnrewrite_log.tsv`), each change
with its rule.

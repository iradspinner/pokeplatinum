# The defensive index

## Summary

A typing's defensive index, from the r/stunfisk post Ian pasted on 2026-11-03, read on Oxide's own type chart and engine and then reweighted by what is used in Oxide. It is a defensive measure only. It says nothing of offence, Speed, a line's moves or its role, so a low index is a reason to look at a line, not a verdict on it.

The post's formula, run on the later games' chart, gives back the post's own single-type ranking for 17 of the 18 types. Grass comes out at -2.5 against the post's -2.0, half a point the post must count somewhere it does not say. Since 2026-11-03 Oxide's chart is the later games' with one change: Ian moved Steel to it that day, so Ghost and Dark hit Steel for neutral damage, and the same day gave Ice a resistance to Water (the [Ice proposal](ice-proposal.md)'s first lever). On it Steel stands at the post's +8.5 and Ice at -4.5, a point above the post's -5.5. Until then Steel kept its Generation 4 resistances to Ghost and Dark (Ian, 2026-09-22) and stood at +11.0. Weighted by what trainers actually attack with in Oxide, Steel is still first, by nearly four points. Ice is 16th of the 18 in the player's view, above Psychic and Rock, and 17th in the trainers', above Psychic.

The four disparities that most change design choices:

1. Steel is in a class of its own. Nine of the ten best typings the player can own have Steel in them (Fighting/Ghost, Annihilape's, is tenth), and the 16 Steel lines average +9.1 in the player's view against +5.9 for Ghost, the next type. Moving Steel to the later chart took 2.8 points off that average (it was +11.8), because Dark is the type trainers attack with most.
2. Ice's lines still average lowest of the 18 types (-1.3 in the player's view; they were -2.5 before Ice resisted Water), with Rock (-0.5) and Psychic (-0.1) the only others below zero. Ice/Rock (Glalie) and Ice/Psychic (Jynx, Mr. Rime) stay near the bottom of the dual typings, since their trouble is the second type's weaknesses, and Grass/Ice (Abomasnow) and pure Ice (Glaceon) are not far above. Ice is also the second most used attacking type against the player. These lines need their niche from offence or Speed.
3. Trainers in Oxide attack with Dark most (about a tenth of all damaging moves, more in the early splits: Bite, Knock Off, Crunch, Sucker Punch), and almost never with Dragon or Fairy (under 2 percent each). So Dragon types defend far better than the post thinks (11th in the post, 5th here), Psychic types worse than the post's figure suggests in the early game, and a Fairy or Dragon weakness costs little.
4. A few lines pair a top typing with a high stat total: Hisuian Goodra (Steel/Dragon, 600), Metagross (605), Magnezone, Steelix (555 and first owned in Gardenia's split), Empoleon and Dusknoir, with Probopass (555, also from Gardenia's split) just behind. Magnezone, with Levitate in one of its two regular slots, has the highest index of any line in the game (+15.9) when it rolls that slot. At the other end, Beautifly, Sudowoodo, Furret, Medicham, Wormadam, Delibird, Frosmoth, Mothim and Kricketune pair a poor typing with a low total, the lines most at risk of having no niche.

Ian asked whether the player's view and the trainers' view differ. Mostly they do not: the rank correlation of the two views is 0.92 over the 18 single types, 0.96 over the 113 dual typings and 0.95 over the 219 lines. Three single types move four places or more, and Normal moves three. Flying is 10th for the player and 5th for a trainer, because trainers attack with Ice, Electric and Rock far more than the player does. Fighting is 8th for the player and 12th for a trainer, because the player hits it with Flying and Psychic more often. Dragon (5th and 9th) and Normal (14th and 11th) move too. Twelve dual typings move 15 places or more, Normal/Flying and Rock/Steel most. No conclusion above changes: Steel is first in both, Ice's lines are last on average in both, and the same lines are flagged.

Decisions for Ian:

1. Decided on 2026-11-03: Steel moves to the later chart, so Ghost and Dark hit it for neutral damage. Steel's index drops from +11.3 to +8.5 in the player's view and it stays first, and every number in this doc is on the new chart.
2. Keep Levitate in one of Magnezone's two regular slots, or move it to the hidden slot: it lifts Magnezone from +9.6 to +15.9, the highest in the game.
3. Read the poor-typing, low-total list in part 4 when the next learnset or stat pass looks at niches; nothing here asks for a change.
4. Say whether the player's hazard terms should run at the post's full 0.5 rather than 0.5 times the share of trainer teams that set each hazard (as built). Full weight moves Fighting from 8th to 5th and Fire from 6th to 9th, and no other type by more than one place.

Next steps: none are required. The script reruns in about 20 seconds after a team, learnset or chart change, and its test could join the gate's balance suites (a few minutes of work) if Ian wants the index kept current.

## What could not be checked

The post's selection of status and hazard terms is read back from its own numbers, since the post gives the formula with "etc.". Its single-type figures are reproduced exactly when it counts burn, poison, paralysis, freeze, powders, Leech Seed and Prankster immunity, the Stealth Rock terms and the Flying type's Spikes and Sticky Web immunity, and not sand, hail, trapping or Toxic Spikes. Grass is the exception, half a point lower than the post has it.

Nothing here was checked in the game; every engine rule is read from the source. Weather Ball is counted as a Normal move and Natural Gift by its listed type, which touches a handful of trainer moves. Abilities that change damage but not by type, such as Multiscale and Ice Scales, are not counted.

The player's lines in parts 3 and 4 are the Box sim's: what a run to the League can catch or be given (its capture areas and the starter), with every evolution reachable by the League's end. That leaves out 21 species the balance tools' wider list has, mostly post-game: Aerodactyl, Anorith and Armaldo, Kabuto and Kabutops, Omanyte and Omastar, Arceus, Darkrai, Dialga, Giratina, Moltres, Palkia, Regice, Regigigas, Regirock, Registeel, Shaymin, Spiritomb, Unown and Zapdos. Every legendary a run can draw is counted, though one run draws only some of them. The player's attacks in the trainers' view come from the balance tools' per-split ownership (`pool.species_by_split` and `pool.moves_at`), which reads the same catches by split.

## Part 1: the post's formula on Oxide's chart

Oxide's chart is the game's own (`pokedex.type_chart`, which reads `sTypeMatchupMultipliers` in `src/battle/battle_lib.c`). Since 2026-11-03 it is the later games' chart, Fairy complete, but for one entry: Water hits Ice at 0.5x (Ian, 2026-11-03, the Ice proposal's first lever), which puts Ice at -4.5 rather than the post's -5.5 in the table of the 18 types below. Until that day it also kept two entries from Generation 4, Ghost and Dark at 0.5x on Steel, which put Steel at +11.0 rather than +8.5.

The status immunities and hazard rules come from Oxide's engine, not the later games'. Every one Ian named holds in Oxide:

| Rule | Where the engine does it |
|---|---|
| Electric types cannot be paralysed | `res/battle/scripts/subscripts/subscript_paralyze.s`, the TYPE_ELECTRIC check ("Electric types cannot be paralysed (Generation 6)") |
| Grass types are immune to powder and spore moves | `src/battle/battle_controller_player.c`, the Move_IsPowder check on a Grass defender; the list is sPowderMoves in `battle_lib.c` |
| Grass types cannot be seeded | `subscript_leech_seed_start.s`, the TYPE_GRASS check |
| Fire types cannot be burned | `subscript_burn.s`, the TYPE_FIRE checks |
| Poison and Steel types cannot be poisoned or badly poisoned | `subscript_poison.s` and `subscript_badly_poison.s` |
| Ice types cannot be frozen | `subscript_freeze.s` |
| Ice types take no hail damage | `src/battle/battle_script.c`, the weather damage command's WEATHER_IS_HAIL block |
| Rock, Ground and Steel types take no sand damage | the same command's WEATHER_IS_SAND block (Rock's Sp. Def rise in sand is not counted) |
| Dark types are immune to a Prankster status move | `battle_controller_player.c`, subscript_prankster_dark_immunity |
| Ghost types cannot be trapped, by Mean Look and the rest or by Shadow Tag and Arena Trap | `battle_controller_player.c` (the PREVENT_ESCAPE check) and `battle_lib.c` ("a Ghost type cannot be trapped by anything") |
| Flying types and Levitate skip Spikes and Toxic Spikes | `subscript_hazards_check.s` (so do an Air Balloon and Magnet Rise; Gravity and an Iron Ball ground them) |
| Sticky Web catches only a grounded Pokemon | `battle_script.c`, BtlCmd_CheckStickyWeb (Battler_IsGrounded) |
| A grounded Poison type takes Toxic Spikes away | `battle_script.c`, BtlCmd_CheckToxicSpikes |
| Stealth Rock does 1/32 to 1/2 by the Rock matchup | `battle_script.c`, BtlCmd_CheckStealthRock |
| Magic Guard skips Spikes, Toxic Spikes and Stealth Rock, but not Sticky Web | `subscript_hazards_check.s` |

Each count in the formula follows from one weakness weight per attacking type: the post's w is 1 for an uncommon coverage type and 2 for a common one, a resistance is worth (1 + w) / 2 and an immunity 1 + w, which gives its 1, 1.5, 2 and 3. A 4x weakness counts as two weaknesses, and a quarter resistance as one and a half resistances (the second halving rarely changes an exchange). The "every engine term" column adds what Oxide's engine does that the post does not count: sand and hail immunity, Ghost's trapping immunity and Toxic Spikes immunity, each at 0.5.

| Rank in Oxide | Type | Post's figure | Post's formula, later chart (check) | Oxide's chart, post's terms | Oxide's chart, every engine term | Post's rank |
|---|---|---|---|---|---|---|
| 1 | Steel | +8.5 | +8.5 | +8.5 | +9.5 | 1 |
| 2 | Ghost | +4.5 | +4.5 | +4.5 | +5.0 | 2 |
| 2 | Fairy | +4.5 | +4.5 | +4.5 | +4.5 | 2 |
| 4 | Poison | +3.5 | +3.5 | +3.5 | +4.0 | 4 |
| 5 | Water | +3.0 | +3.0 | +3.0 | +3.0 | 5 |
| 6 | Fire | +2.5 | +2.5 | +2.5 | +2.5 | 6 |
| 7 | Fighting | +2.0 | +2.0 | +2.0 | +2.0 | 7 |
| 7 | Flying | +2.0 | +2.0 | +2.0 | +2.5 | 7 |
| 9 | Electric | +1.5 | +1.5 | +1.5 | +1.5 | 9 |
| 10 | Ground | +1.0 | +1.0 | +1.0 | +1.5 | 10 |
| 11 | Dragon | +0.5 | +0.5 | +0.5 | +0.5 | 11 |
| 12 | Normal | 0.0 | 0.0 | 0.0 | 0.0 | 12 |
| 12 | Dark | 0.0 | 0.0 | 0.0 | 0.0 | 12 |
| 14 | Bug | -1.5 | -1.5 | -1.5 | -1.5 | 14 |
| 15 | Grass | -2.0 | -2.5 | -2.5 | -2.5 | 15 |
| 15 | Psychic | -2.5 | -2.5 | -2.5 | -2.5 | 16 |
| 15 | Rock | -2.5 | -2.5 | -2.5 | -2.0 | 16 |
| 18 | Ice | -5.5 | -5.5 | -4.5 | -4.0 | 18 |

## Part 2: weighted by what is used in Oxide

### How the weights are set

The post's fixed common-coverage list becomes a weight for each attacking type taken from use. The post's structure is kept exactly: the weakness weight w carries the use, a resistance is worth (1 + w) / 2 and an immunity 1 + w. The weakness weights are w = 25 times the type's share of the attacks counted, so the 18 weights still sum to the post's 25, a type used at the average rate weighs 1.39, and shares in the post's own ratio (2 for a common coverage type, 1 for the rest) give back the post's weights exactly (the test checks this). A type nobody uses still gives a resistance half a point, which is the post's own floor.

Each split's shares are worked out on their own, and the overall, early, middle and late weights are the plain mean of their splits' shares, so a long split with many trainers does not outweigh a short one. Early is Roark to Maylene, middle Wake to HQ, late Galactic to the League.

Ian asked for two views (2026-11-03).

The player's view is how the player's Pokemon defend, against what trainers attack with. Every damaging move on every trainer team in `res/trainers/data` that the player fights in the twelve splits is counted, with the type the engine gives it: Hidden Power by the IVs (Move_CalcVariableType), Judgment by the plate, Pixilate's Normal moves as Fairy, Normalize's moves as Normal, Liquid Voice's sound moves as Water (BattleSystem_SetMoveTypeByAbility). Ten Hidden Powers, two Hyper Voices and one Quick Attack change type this way. Each move is weighted by its trainer's kind: a boss counts 3, a mini-boss 2 and an ordinary trainer 1. Bosses are the fights in `tools/oxide/balance/fights.json` other than the named Galactic officers' (rivals, commanders, Cyrus, leaders, Frontier Brains, the League); mini-bosses are the officers' fights, the Ace Trainers and the gauntlet sections' trainers. A rival fight's teams (one for each starter, and Lucas or Dawn) share the fight's weight, so each fight counts once, and a tag fight's partners are left out. That is 524 teams, 1,876 Pokemon and 5,475 damaging moves.

The trainers' view is how a trainer's Pokemon defend, against what the player attacks with. For each split, every line the player can own by its end (its most evolved stage then) counts each type it can hit with once: a damaging move of power 40 or more, or one whose power the engine works out, among its level-up moves by the capture rule and the TMs and tutors placed by then. Moves the balance tools already call unreliable or a sacrifice are left out. Normal weighs most here (3.47 overall, 5.07 early), because nearly every line learns a Normal attack, though few would choose it as a main attack; that lifts Ghost, Rock and Steel a little in this view.

The situational terms (Stealth Rock, Spikes and Sticky Web, Toxic Spikes, Prankster, trapping, sand and hail) matter only when the other side brings the thing. In the player's view each is the post's 0.5 times the share of the split's trainer teams that bring it, weighted by kind, as Ian asked: the player switches often, so a hazard on the field costs in full, and the share says how often one is there. A team brings a hazard if any member knows the move, sand or hail if a member sets it or the map's weather does (`splits.trainer_weather`), trapping if a member knows a trapping move or has Shadow Tag or Arena Trap. In the trainers' view each is a flat 0.05, a tenth of the post's figure, and sand and hail are 0. The player rarely spends a turn on a hazard and the AI switches only on a knockout or a pivot, so a hazard meets each trainer Pokemon at most once; a tenth keeps the terms' sign without letting them move a rank alone, and the player sets no weather at all (the standing ruling).

### What trainers attack with, by split (percent of the kind-weighted damaging moves)

| Type | Roark | Gardenia | Fantina | Maylene | Wake | Byron | Candice | HQ | Galactic | Volkner | Barry | League |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Normal | 14 | 14 | 7 | 10 | 7 | 6 | 6 | 8 | 7 | 7 | 7 | 3 |
| Fire | 4 | 3 | 3 | 5 | 5 | 5 | 6 | 5 | 6 | 3 | 7 | 10 |
| Water | 10 | 6 | 4 | 6 | 14 | 6 | 5 | 4 | 5 | 8 | 9 | 2 |
| Electric | 4 | 4 | 7 | 6 | 5 | 4 | 5 | 5 | 5 | 32 | 6 | 5 |
| Grass | 4 | 11 | 6 | 6 | 5 | 4 | 5 | 4 | 4 | 3 | 3 | 5 |
| Ice | 4 | 4 | 3 | 7 | 9 | 8 | 20 | 9 | 9 | 7 | 11 | 5 |
| Fighting | 7 | 4 | 6 | 13 | 5 | 9 | 7 | 7 | 9 | 8 | 11 | 10 |
| Poison | 4 | 4 | 5 | 3 | 5 | 3 | 4 | 5 | 3 | 0 | 2 | 4 |
| Ground | 6 | 3 | 5 | 3 | 7 | 7 | 8 | 9 | 11 | 3 | 11 | 12 |
| Flying | 4 | 4 | 4 | 3 | 4 | 4 | 3 | 2 | 4 | 1 | 3 | 2 |
| Psychic | 3 | 7 | 5 | 5 | 5 | 4 | 5 | 5 | 5 | 1 | 6 | 8 |
| Bug | 4 | 7 | 6 | 6 | 3 | 4 | 4 | 7 | 6 | 7 | 5 | 10 |
| Rock | 14 | 7 | 5 | 6 | 4 | 6 | 3 | 5 | 7 | 2 | 5 | 8 |
| Ghost | 1 | 3 | 11 | 3 | 4 | 3 | 6 | 5 | 3 | 5 | 2 | 3 |
| Dragon | 0 | 0 | 1 | 1 | 2 | 2 | 1 | 2 | 2 | 1 | 2 | 2 |
| Dark | 12 | 13 | 18 | 10 | 10 | 13 | 7 | 12 | 11 | 4 | 7 | 8 |
| Steel | 2 | 2 | 2 | 3 | 2 | 9 | 2 | 4 | 2 | 6 | 1 | 5 |
| Fairy | 2 | 2 | 3 | 3 | 3 | 3 | 2 | 3 | 0 | 0 | 0 | 0 |

### What the player can attack with, by split (percent of line-and-type pairs)

| Type | Roark | Gardenia | Fantina | Maylene | Wake | Byron | Candice | HQ | Galactic | Volkner | Barry | League |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Normal | 26 | 23 | 18 | 15 | 12 | 11 | 10 | 11 | 10 | 10 | 10 | 10 |
| Fire | 4 | 2 | 2 | 2 | 3 | 4 | 4 | 4 | 4 | 4 | 4 | 4 |
| Water | 11 | 7 | 7 | 6 | 5 | 4 | 5 | 4 | 5 | 4 | 4 | 4 |
| Electric | 2 | 4 | 4 | 5 | 5 | 5 | 5 | 5 | 4 | 4 | 4 | 4 |
| Grass | 4 | 4 | 4 | 6 | 5 | 5 | 5 | 5 | 6 | 6 | 6 | 6 |
| Ice | 2 | 4 | 4 | 4 | 6 | 6 | 6 | 6 | 6 | 6 | 6 | 6 |
| Fighting | 2 | 8 | 7 | 7 | 6 | 5 | 5 | 5 | 6 | 6 | 6 | 6 |
| Poison | 5 | 3 | 4 | 4 | 4 | 4 | 3 | 4 | 4 | 4 | 4 | 4 |
| Ground | 3 | 4 | 10 | 9 | 7 | 7 | 7 | 7 | 6 | 6 | 6 | 6 |
| Flying | 9 | 7 | 5 | 6 | 6 | 5 | 5 | 5 | 5 | 5 | 5 | 5 |
| Psychic | 3 | 4 | 3 | 5 | 4 | 5 | 6 | 6 | 5 | 5 | 5 | 5 |
| Bug | 4 | 4 | 5 | 4 | 8 | 7 | 7 | 7 | 7 | 7 | 7 | 7 |
| Rock | 11 | 9 | 8 | 7 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 |
| Ghost | 1 | 1 | 5 | 4 | 7 | 6 | 6 | 6 | 6 | 6 | 6 | 6 |
| Dragon | 1 | 1 | 1 | 1 | 2 | 2 | 2 | 2 | 3 | 3 | 3 | 3 |
| Dark | 8 | 11 | 10 | 10 | 10 | 9 | 9 | 9 | 8 | 8 | 8 | 8 |
| Steel | 1 | 2 | 2 | 2 | 3 | 6 | 6 | 6 | 6 | 6 | 6 | 6 |
| Fairy | 1 | 2 | 2 | 2 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 |

### The weakness weights (w; the post's are 1 and 2)

| Type | Post | Player's view, overall | Player's view, early | Player's view, middle | Player's view, late | Trainers' view, overall | Trainers' view, early | Trainers' view, middle | Trainers' view, late |
|---|---|---|---|---|---|---|---|---|---|
| Normal | 1 | 2.02 | 2.83 | 1.68 | 1.55 | 3.47 | 5.07 | 2.73 | 2.60 |
| Fire | 2 | 1.29 | 0.91 | 1.34 | 1.62 | 0.89 | 0.60 | 0.99 | 1.07 |
| Water | 1 | 1.64 | 1.61 | 1.81 | 1.49 | 1.38 | 1.89 | 1.14 | 1.12 |
| Electric | 1 | 1.84 | 1.30 | 1.24 | 2.99 | 1.04 | 0.89 | 1.15 | 1.09 |
| Grass | 1 | 1.24 | 1.65 | 1.12 | 0.94 | 1.29 | 1.18 | 1.24 | 1.44 |
| Ice | 2 | 2.03 | 1.18 | 2.88 | 2.05 | 1.27 | 0.88 | 1.48 | 1.45 |
| Fighting | 2 | 2.00 | 1.88 | 1.81 | 2.31 | 1.41 | 1.48 | 1.33 | 1.41 |
| Poison | 1 | 0.92 | 1.09 | 1.06 | 0.60 | 0.98 | 1.06 | 0.88 | 0.98 |
| Ground | 2 | 1.77 | 1.12 | 1.90 | 2.29 | 1.65 | 1.64 | 1.72 | 1.60 |
| Flying | 1 | 0.82 | 0.89 | 0.89 | 0.68 | 1.41 | 1.67 | 1.33 | 1.22 |
| Psychic | 1 | 1.21 | 1.21 | 1.16 | 1.27 | 1.20 | 0.93 | 1.31 | 1.35 |
| Bug | 2 | 1.44 | 1.43 | 1.13 | 1.75 | 1.51 | 1.11 | 1.76 | 1.65 |
| Rock | 2 | 1.51 | 2.00 | 1.12 | 1.40 | 1.58 | 2.13 | 1.33 | 1.28 |
| Ghost | 1 | 1.03 | 1.14 | 1.09 | 0.85 | 1.29 | 0.70 | 1.65 | 1.52 |
| Dragon | 1 | 0.36 | 0.17 | 0.42 | 0.49 | 0.48 | 0.35 | 0.41 | 0.68 |
| Dark | 2 | 2.59 | 3.32 | 2.65 | 1.80 | 2.25 | 2.46 | 2.25 | 2.03 |
| Steel | 1 | 0.86 | 0.62 | 1.06 | 0.91 | 1.13 | 0.45 | 1.36 | 1.57 |
| Fairy | 1 | 0.44 | 0.66 | 0.65 | 0.02 | 0.79 | 0.50 | 0.93 | 0.94 |

### Trainer teams that bring each situational term, by split

| Split | Teams | Stealth Rock teams | Spikes teams | Toxic Spikes teams | Sticky Web teams | Stealth Rock % | Spikes or Web % | Toxic Spikes % | Sand % | Hail % | Trapping % | Prankster % |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Roark | 45 | 7 | 3 | 0 | 0 | 20 | 7 | 0 | 14 | 0 | 0 | 0 |
| Gardenia | 41 | 6 | 2 | 2 | 1 | 17 | 6 | 4 | 0 | 2 | 0 | 6 |
| Fantina | 49 | 11 | 1 | 5 | 1 | 16 | 4 | 16 | 0 | 2 | 5 | 9 |
| Maylene | 46 | 4 | 3 | 2 | 3 | 8 | 12 | 8 | 2 | 0 | 2 | 8 |
| Wake | 76 | 5 | 3 | 7 | 1 | 6 | 7 | 12 | 1 | 0 | 5 | 5 |
| Byron | 69 | 24 | 11 | 7 | 1 | 39 | 20 | 10 | 3 | 0 | 7 | 14 |
| Candice | 27 | 6 | 7 | 1 | 0 | 27 | 27 | 6 | 0 | 62 | 0 | 8 |
| HQ | 30 | 9 | 5 | 1 | 1 | 32 | 22 | 4 | 2 | 0 | 6 | 8 |
| Galactic | 71 | 8 | 1 | 4 | 0 | 11 | 2 | 8 | 12 | 1 | 7 | 0 |
| Volkner | 22 | 1 | 1 | 0 | 0 | 12 | 12 | 0 | 0 | 0 | 4 | 0 |
| Barry | 38 | 5 | 1 | 6 | 0 | 12 | 4 | 6 | 2 | 0 | 0 | 0 |
| League | 10 | 5 | 2 | 1 | 0 | 65 | 30 | 15 | 20 | 0 | 0 | 0 |

The situational weights that result:

| View | stealth rock | spikes web | toxic spikes | prankster | trap | sand | hail |
|---|---|---|---|---|---|---|---|
| player, overall | 0.111 | 0.064 | 0.037 | 0.024 | 0.015 | 0.024 | 0.028 |
| trainer, overall | 0.050 | 0.050 | 0.050 | 0.050 | 0.050 | 0.000 | 0.000 |
| player, early | 0.077 | 0.035 | 0.035 | 0.029 | 0.009 | 0.019 | 0.005 |
| player, middle | 0.130 | 0.096 | 0.041 | 0.043 | 0.022 | 0.008 | 0.078 |
| player, late | 0.125 | 0.059 | 0.036 | 0.000 | 0.013 | 0.043 | 0.001 |

### The 18 single types, ranked by the player's view (each view's rank in brackets)

| Type | Post's terms | Player, overall | Player, early | Player, middle | Player, late | Trainer, overall | Trainer, early | Trainer, middle | Trainer, late |
|---|---|---|---|---|---|---|---|---|---|
| Steel | +8.5 | +8.50 (1) | +10.13 (1) | +8.75 (1) | +6.61 (1) | +10.68 (1) | +11.08 (1) | +10.39 (1) | +10.58 (1) |
| Ghost | +4.5 | +4.60 (2) | +4.52 (2) | +3.86 (2) | +5.40 (2) | +5.63 (2) | +7.53 (2) | +4.53 (2) | +4.83 (2) |
| Fairy | +4.5 | +4.09 (3) | +4.27 (3) | +3.59 (3) | +4.41 (3) | +3.46 (3) | +3.86 (3) | +3.35 (3) | +3.16 (5) |
| Poison | +3.5 | +3.08 (4) | +4.07 (4) | +2.87 (5) | +2.29 (5) | +3.18 (4) | +3.14 (4) | +3.09 (5) | +3.30 (4) |
| Dragon | +0.5 | +2.17 (5) | +2.73 (5) | +0.80 (11) | +2.97 (4) | +1.76 (9) | +2.56 (5) | +1.43 (9) | +1.30 (9) |
| Fire | +2.5 | +2.13 (6) | +1.91 (8) | +2.62 (6) | +1.84 (8) | +2.27 (6) | +0.15 (14) | +3.14 (4) | +3.51 (3) |
| Electric | +1.5 | +1.99 (7) | +2.29 (6) | +1.70 (7) | +2.00 (7) | +2.13 (7) | +1.87 (7) | +2.20 (7) | +2.34 (7) |
| Fighting | +2.0 | +1.90 (8) | +2.19 (7) | +1.38 (9) | +2.13 (6) | +0.82 (12) | +1.30 (10) | +0.65 (12) | +0.51 (12) |
| Water | +3.0 | +1.83 (9) | +1.20 (11) | +3.19 (4) | +1.10 (10) | +2.00 (8) | +1.84 (8) | +2.10 (8) | +2.07 (8) |
| Flying | +2.0 | +1.21 (10) | +1.61 (9) | +1.19 (10) | +0.82 (11) | +2.41 (5) | +2.17 (6) | +2.47 (6) | +2.59 (6) |
| Dark | 0.0 | +1.16 (11) | +1.49 (10) | +1.49 (8) | +0.50 (12) | +1.31 (10) | +1.47 (9) | +1.29 (11) | +1.18 (10) |
| Ground | +1.0 | +0.28 (12) | +0.51 (12) | -1.34 (15) | +1.68 (9) | +0.43 (13) | +0.58 (11) | +0.44 (13) | +0.26 (13) |
| Bug | -1.5 | +0.27 (13) | -0.05 (15) | +0.43 (12) | +0.44 (13) | -0.25 (14) | -0.80 (16) | -0.06 (14) | +0.11 (14) |
| Normal | 0.0 | +0.03 (14) | +0.26 (14) | +0.29 (13) | -0.46 (15) | +0.88 (11) | +0.22 (13) | +1.32 (10) | +1.11 (11) |
| Grass | -2.5 | -0.26 (15) | +0.35 (13) | -1.27 (14) | +0.15 (14) | -0.36 (15) | +0.49 (12) | -0.83 (15) | -0.74 (15) |
| Ice | -4.5 | -2.40 (16) | -2.58 (17) | -1.53 (16) | -3.10 (17) | -2.22 (17) | -1.83 (17) | -2.24 (17) | -2.60 (17) |
| Psychic | -2.5 | -2.45 (17) | -3.34 (18) | -2.39 (17) | -1.61 (16) | -2.74 (18) | -2.06 (18) | -3.35 (18) | -2.81 (18) |
| Rock | -2.5 | -2.96 (18) | -2.00 (16) | -3.20 (18) | -3.67 (18) | -1.49 (16) | -0.45 (15) | -1.81 (16) | -2.21 (16) |

Ranks that change with every situational term at the full 0.5: Normal 14 to 13; Fire 6 to 9; Water 9 to 8; Fighting 8 to 5; Bug 13 to 14; Dragon 5 to 6.

## Part 3: dual typings

Every typing an obtainable stage has, scored in both views with the overall weights. "Fielded by trainers" is the kind-weighted count of trainer Pokemon of that typing, so the trainers' view can be read for the typings trainers actually use; the most fielded are pure Normal (186), pure Water (105), pure Fire (86) and pure Fighting (80).

Typings: 113. Rank correlation (Spearman) of the player's view with the trainers' view: 0.96; with the post's formula: 0.95. Typings moving 15 places or more between the views: 12.

### The best twenty, by the player's view

| Rank | Typing | Player's view | Trainers' view | Trainers' rank | Post's formula | Post's rank | Fielded by trainers (weighted) | Obtainable stages |
|---|---|---|---|---|---|---|---|---|
| 1 | Steel/Fairy | +12.65 | +14.01 | 2 | +12.8 | 1 | 24 | Klefki, Mawile |
| 2 | Flying/Steel | +11.54 | +14.13 | 1 | +12.8 | 1 | 25 | Corviknite, Skarmory |
| 3 | Dragon/Steel | +10.17 | +11.59 | 6 | +9.5 | 4 | 0 | Hisuian Goodra, Hisuian Sliggoo |
| 4 | Grass/Steel | +9.63 | +11.64 | 5 | +8.0 | 7 | 13 | Ferroseed, Ferrothorn |
| 5 | Electric/Steel | +9.57 | +11.68 | 3 | +9.0 | 5 | 26 | Magnemite, Magneton, Magnezone, Togedemaru |
| 6 | Water/Steel | +9.37 | +11.67 | 4 | +10.8 | 3 | 13 | Empoleon |
| 7 | Bug/Steel | +9.26 | +10.88 | 7 | +8.0 | 7 | 23 | Scizor |
| 8 | Fighting/Steel | +8.84 | +10.40 | 8 | +8.8 | 6 | 19 | Lucario |
| 9 | Ground/Steel | +7.75 | +9.73 | 9 | +8.0 | 7 | 12 | Steelix |
| 10 | Fighting/Ghost | +6.68 | +6.44 | 16 | +6.2 | 15 | 3 | Annihilape |
| 11 | Dragon/Fairy | +6.62 | +5.70 | 20 | +6.0 | 18 | 6 | Altaria |
| 12 | Electric/Ghost | +6.59 | +7.76 | 11 | +6.0 | 18 | 16 | Rotom |
| 13 | Water/Ghost | +6.43 | +7.63 | 12 | +7.5 | 10 | 10 | Frillish, Jellicent |
| 14 | Psychic/Steel | +6.22 | +7.85 | 10 | +6.5 | 12 | 45 | Bronzong, Bronzor, Metagross, Metang |
| 15 | Fire/Ghost | +6.11 | +7.27 | 13 | +6.2 | 15 | 5 | Ceruledge, Chandelure, Lampent, Litwick |
| 16 | Poison/Dark | +5.89 | +6.04 | 19 | +5.5 | 21 | 30 | Drapion, Skuntank, Stunky |
| 17 | Water/Fairy | +5.85 | +5.52 | 23 | +7.5 | 10 | 19 | Alomomola, Azumarill, Luvdisc, Marill, Primarina |
| 18 | Poison/Fairy | +5.77 | +5.39 | 26 | +6.5 | 12 | 5 | Galarian Weezing |
| 19 | Fire/Fairy | +5.54 | +5.16 | 29 | +6.2 | 15 | 17 | Galarian Rapidash, Ninetales |
| 20 | Electric/Flying | +5.40 | +6.22 | 17 | +5.5 | 21 | 6 | Emolga |

### The worst twenty, by the player's view

| Rank | Typing | Player's view | Trainers' view | Trainers' rank | Post's formula | Post's rank | Fielded by trainers (weighted) | Obtainable stages |
|---|---|---|---|---|---|---|---|---|
| 94 | Psychic/Dark | -1.08 | -1.56 | 103 | -2.5 | 93 | 7 | Gothitelle |
| 95 | Flying/Bug | -1.21 | -0.34 | 91 | -2.2 | 91 | 30 | Beautifly, Combee, Mothim, Scyther, Vespiquen and 3 more |
| 96 | Grass/Bug | -1.23 | -1.85 | 105 | -5.2 | 109 | 8 | Leavanny, Sewaddle, Swadloon, Wormadam |
| 97 | Ice/Dark | -1.24 | -0.91 | 96 | -4.5 | 105 | 15 | Sneasel, Weavile |
| 98 | Fire/Rock | -1.35 | +0.51 | 83 | -0.8 | 84 | 3 | Magcargo |
| 99 | Water/Rock | -1.45 | +0.30 | 86 | -0.2 | 83 | 23 | Corsola, Relicanth |
| 100 | Bug/Rock | -1.62 | -0.92 | 97 | -2.5 | 93 | 16 | Crustle, Dwebble, Kleavor |
| 101 | Ice/Bug | -1.63 | -2.27 | 107 | -5.5 | 110 | 3 | Frosmoth, Snom |
| 102 | Rock/Dark | -1.79 | -0.18 | 87 | -2.5 | 93 | 7 | Tyranitar |
| 103 | Water/Ice | -1.91 | -1.38 | 101 | -2.2 | 91 | 40 | Cloyster, Dewgong, Lapras, Sealeo, Spheal and 1 more |
| 104 | Grass/Rock | -2.38 | -1.06 | 99 | -4.0 | 104 | 7 | Cradily, Lileep |
| 105 | Ice | -2.40 | -2.22 | 106 | -4.5 | 105 | 12 | Glaceon, Snorunt |
| 106 | Psychic | -2.45 | -2.74 | 108 | -2.5 | 93 | 54 | Abra, Alakazam, Chimecho, Chingling, Cresselia and 4 more |
| 107 | Grass/Ice | -2.80 | -3.05 | 109 | -7.0 | 113 | 14 | Abomasnow, Snover |
| 108 | Psychic/Bug | -2.92 | -3.59 | 111 | -4.8 | 108 | 3 | Dottler, Orbeetle |
| 109 | Rock | -2.96 | -1.49 | 102 | -2.5 | 93 | 29 | Bonsly, Cranidos, Garganacl, Nacli, Naclstack and 3 more |
| 110 | Ground/Rock | -3.18 | -1.56 | 104 | -2.0 | 89 | 30 | Geodude, Golem, Graveler, Onix, Rhydon and 2 more |
| 111 | Ice/Psychic | -4.35 | -4.76 | 113 | -6.5 | 111 | 14 | Galarian Mr Mime, Jynx, Mr. Rime, Smoochum |
| 112 | Ice/Rock | -4.89 | -3.58 | 110 | -6.5 | 111 | 11 | Glalie |
| 113 | Psychic/Rock | -4.90 | -4.03 | 112 | -4.5 | 105 | 10 | Lunatone, Solrock |

### Typings that move 15 places or more between the two views

| Typing | Player's rank | Trainers' rank | Player's view | Trainers' view |
|---|---|---|---|---|
| Normal/Flying | 71 | 40 | +1.74 | +3.50 |
| Rock/Steel | 44 | 14 | +3.54 | +6.63 |
| Flying/Ghost | 41 | 18 | +3.70 | +6.21 |
| Fighting/Dragon | 33 | 56 | +4.07 | +2.58 |
| Fighting/Bug | 56 | 77 | +2.43 | +0.86 |
| Fighting/Psychic | 79 | 98 | +0.57 | -0.94 |
| Flying | 75 | 58 | +1.21 | +2.41 |
| Normal/Water | 69 | 52 | +1.86 | +2.89 |
| Water/Fighting | 38 | 53 | +3.73 | +2.82 |
| Water/Dragon | 35 | 50 | +3.82 | +3.00 |
| Fire/Rock | 98 | 83 | -1.35 | +0.51 |
| Rock/Dark | 102 | 87 | -1.79 | -0.18 |

## Part 4: each line's final stage, against its stats

Each obtainable line's final stage (a branching line has one row a branch; Mega forms are left out), with its abilities. An ability counts only when every regular slot holds it; an ability in one of two regular slots, or in the hidden slot, is listed with the index it would give. The abilities counted, each from Oxide's engine: Levitate, Flash Fire, Water Absorb, Storm Drain, Dry Skin (Water immunity, and Fire at 1.25 times), Volt Absorb, Motor Drive, Lightning Rod and Sap Sipper (BattleSystem_TriggerImmunityAbility in `battle_lib.c`); Thick Fat, Heatproof, Water Bubble, Purifying Salt and Fluffy (the damage formula); Filter and Solid Rock (super-effective damage at three quarters); Wonder Guard; and the status abilities the subscripts check (Limber, Water Veil, Water Bubble, Immunity, Pastel Veil, Magma Armor, Purifying Salt, Overcoat), with the sand and hail abilities and Magic Guard. Of the 219 lines, 37 have a counted ability and 68 have one that does not count.

"Placement" is the line's index and its bulk (HP plus Def plus SpD) added as standard scores across the 219 lines, so a line high on both is the most defensively placed. The index is the player's view with the overall weights.

### The twenty most defensively placed lines

| Line | Typing | Index, player's view | Index, trainers' view | BST | HP | Def | SpD | Spe | First owned | Placement | Abilities |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Steelix | Steel/Ground | +7.75 | +9.73 | 555 | 100 | 200 | 75 | 30 | Gardenia | +4.30 | Solid Rock (one slot, +10.5) |
| Skarmory | Steel/Flying | +12.84 | +14.93 | 500 | 85 | 140 | 80 | 70 | Galactic | +4.26 | Filter (counted) |
| Dusknoir | Ghost | +7.47 | +8.38 | 555 | 105 | 135 | 135 | 45 | Candice | +4.21 | Levitate (counted) |
| Hisuian Goodra | Steel/Dragon | +10.17 | +11.59 | 600 | 80 | 100 | 150 | 60 | Byron | +4.01 | Sap Sipper (one slot, +10.7) |
| Ferrothorn | Grass/Steel | +9.63 | +11.64 | 489 | 74 | 131 | 116 | 20 | Wake | +3.64 |  |
| Corviknite | Flying/Steel | +11.54 | +14.13 | 495 | 98 | 105 | 85 | 67 | Wake | +3.47 |  |
| Probopass | Rock/Steel | +5.79 | +8.48 | 555 | 70 | 145 | 150 | 40 | Gardenia | +3.47 | Solid Rock (counted) |
| Bastiodon | Rock/Steel | +3.54 | +6.63 | 515 | 80 | 168 | 138 | 30 | Fantina | +3.26 | Solid Rock (one slot, +5.8) |
| Rotom | Electric/Ghost | +11.23 | +12.17 | 525 | 50 | 107 | 107 | 91 | Fantina | +2.83 | Levitate (counted) |
| Toxapex | Poison/Water | +5.02 | +5.33 | 495 | 50 | 152 | 142 | 35 | Maylene | +2.75 | Limber (one slot, +5.5) |
| Klefki | Steel/Fairy | +12.65 | +14.01 | 470 | 57 | 91 | 87 | 75 | Fantina | +2.60 |  |
| Empoleon | Water/Steel | +9.37 | +11.67 | 535 | 84 | 93 | 101 | 60 | Maylene | +2.58 |  |
| Magnezone | Electric/Steel | +9.57 | +11.68 | 535 | 70 | 115 | 90 | 60 | Byron | +2.57 | Levitate (one slot, +15.9) |
| Blissey | Normal | +0.03 | +0.88 | 540 | 255 | 10 | 135 | 55 | Wake | +2.50 |  |
| Mawile | Steel/Fairy | +12.65 | +14.01 | 440 | 70 | 85 | 75 | 50 | Byron | +2.49 |  |
| Bronzong | Steel/Psychic | +6.22 | +7.85 | 530 | 77 | 116 | 116 | 33 | Fantina | +2.32 | Levitate (one slot, +10.8); Heatproof (one slot, +7.5) |
| Metagross | Steel/Psychic | +6.22 | +7.85 | 605 | 80 | 130 | 90 | 70 | Byron | +2.12 |  |
| Cresselia | Psychic | +0.42 | +0.01 | 600 | 120 | 120 | 130 | 85 | Volkner | +1.94 | Levitate (counted) |
| Scizor | Bug/Steel | +9.26 | +10.88 | 500 | 70 | 100 | 80 | 65 | Maylene | +1.91 |  |
| Weezing | Poison | +7.68 | +7.54 | 510 | 65 | 120 | 85 | 60 | Maylene | +1.88 | Levitate (counted) |

### The twenty least defensively placed lines

| Line | Typing | Index, player's view | Index, trainers' view | BST | HP | Def | SpD | Spe | First owned | Placement | Abilities |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Beautifly | Bug/Flying | -1.21 | -0.34 | 395 | 60 | 50 | 50 | 65 | Roark | -3.35 |  |
| Alakazam | Psychic | -2.45 | -2.74 | 490 | 55 | 45 | 85 | 120 | Wake | -3.16 | Magic Guard (hidden, -2.2) |
| Glalie | Ice/Rock | -4.89 | -3.58 | 520 | 80 | 80 | 80 | 100 | Wake | -2.65 | Solid Rock (one slot, -1.8) |
| Jynx | Ice/Psychic | -4.35 | -4.76 | 495 | 65 | 57 | 113 | 95 | Fantina | -2.60 | Snow Cloak (counted); Dry Skin (hidden, -3.4) |
| Pheromosa | Bug/Fighting | +2.43 | +0.86 | 570 | 71 | 37 | 37 | 151 | Volkner | -2.58 |  |
| Delibird | Ice/Flying | -0.17 | +0.53 | 460 | 65 | 60 | 60 | 100 | Candice | -2.46 |  |
| Mothim | Bug/Flying | -1.21 | -0.34 | 464 | 80 | 60 | 60 | 76 | Gardenia | -2.44 |  |
| Chatot | Normal/Flying | +1.74 | +3.50 | 466 | 76 | 45 | 42 | 110 | Maylene | -2.38 |  |
| Espeon | Psychic | -2.45 | -2.74 | 525 | 65 | 60 | 95 | 110 | Byron | -2.36 |  |
| Sharpedo | Water/Dark | +2.99 | +3.32 | 460 | 70 | 40 | 40 | 95 | Fantina | -2.29 |  |
| Cinccino | Normal | +0.03 | +0.88 | 470 | 75 | 60 | 60 | 115 | Wake | -2.18 |  |
| Mr. Rime | Ice/Psychic | -4.35 | -4.76 | 520 | 80 | 75 | 100 | 70 | Wake | -2.15 |  |
| Frosmoth | Ice/Bug | -1.63 | -2.27 | 475 | 70 | 60 | 90 | 65 | Candice | -2.11 |  |
| Minun | Electric | +1.99 | +2.13 | 415 | 65 | 55 | 55 | 105 | Gardenia | -2.03 | Volt Absorb (hidden, +3.4) |
| Weavile | Dark/Ice | -1.24 | -0.91 | 510 | 70 | 65 | 85 | 125 | HQ | -1.99 |  |
| Furret | Normal | +0.03 | +0.88 | 425 | 85 | 64 | 55 | 90 | Roark | -1.97 |  |
| Absol | Dark | +1.16 | +1.31 | 530 | 70 | 60 | 60 | 95 | Wake | -1.94 |  |
| Rampardos | Rock | -2.96 | -1.49 | 500 | 97 | 80 | 70 | 58 | Fantina | -1.90 |  |
| Ambipom | Normal | +0.03 | +0.88 | 482 | 75 | 66 | 66 | 115 | Fantina | -1.90 |  |
| Liepard | Dark | +1.16 | +1.31 | 496 | 74 | 60 | 60 | 116 | Gardenia | -1.85 | Limber (one slot, +1.7) |

### A strong typing on a high stat total: the lines most likely too strong

Both the index and the stat total half a standard deviation or more above the mean.

| Line | Typing | Index, player's view | Index, trainers' view | BST | HP | Def | SpD | Spe | First owned | Abilities |
|---|---|---|---|---|---|---|---|---|---|---|
| Hisuian Goodra | Steel/Dragon | +10.17 | +11.59 | 600 | 80 | 100 | 150 | 60 | Byron | Sap Sipper (one slot, +10.7) |
| Metagross | Steel/Psychic | +6.22 | +7.85 | 605 | 80 | 130 | 90 | 70 | Byron |  |
| Magnezone | Electric/Steel | +9.57 | +11.68 | 535 | 70 | 115 | 90 | 60 | Byron | Levitate (one slot, +15.9) |
| Steelix | Steel/Ground | +7.75 | +9.73 | 555 | 100 | 200 | 75 | 30 | Gardenia | Solid Rock (one slot, +10.5) |
| Empoleon | Water/Steel | +9.37 | +11.67 | 535 | 84 | 93 | 101 | 60 | Maylene |  |
| Dusknoir | Ghost | +7.47 | +8.38 | 555 | 105 | 135 | 135 | 45 | Candice | Levitate (counted) |
| Ninetales | Fire/Fairy | +5.88 | +5.31 | 555 | 85 | 84 | 117 | 95 | Maylene | Magic Guard (counted) |
| Probopass | Rock/Steel | +5.79 | +8.48 | 555 | 70 | 145 | 150 | 40 | Gardenia | Solid Rock (counted) |
| Annihilape | Fighting/Ghost | +6.68 | +6.44 | 535 | 110 | 80 | 90 | 90 | Byron |  |
| Bronzong | Steel/Psychic | +6.22 | +7.85 | 530 | 77 | 116 | 116 | 33 | Fantina | Levitate (one slot, +10.8); Heatproof (one slot, +7.5) |
| Primarina | Water/Fairy | +5.85 | +5.52 | 530 | 80 | 74 | 116 | 60 | Maylene |  |
| Galarian Rapidash | Fairy/Fire | +5.54 | +5.16 | 530 | 80 | 85 | 95 | 95 | Gardenia | Pastel Veil (one slot, +6.1) |
| Tentacruel | Water/Poison | +5.02 | +5.33 | 535 | 80 | 65 | 120 | 100 | Fantina |  |
| Swampert | Water/Ground | +4.79 | +3.80 | 535 | 100 | 90 | 90 | 60 | Maylene |  |
| Decidueye | Grass/Ghost | +4.52 | +5.51 | 530 | 78 | 75 | 100 | 70 | Maylene |  |

### A poor typing on a low stat total: the lines most likely to have no niche

Both half a standard deviation or more below the mean. Several are fast or hit hard, which the index cannot see.

| Line | Typing | Index, player's view | Index, trainers' view | BST | HP | Def | SpD | Spe | First owned | Abilities |
|---|---|---|---|---|---|---|---|---|---|---|
| Beautifly | Bug/Flying | -1.21 | -0.34 | 395 | 60 | 50 | 50 | 65 | Roark |  |
| Sudowoodo | Rock | -2.96 | -1.49 | 450 | 85 | 115 | 80 | 30 | Fantina |  |
| Furret | Normal | +0.03 | +0.88 | 425 | 85 | 64 | 55 | 90 | Roark |  |
| Wormadam | Bug/Grass | -1.23 | -1.85 | 444 | 60 | 85 | 105 | 36 | Gardenia | Overcoat (one slot, -1.2) |
| Medicham | Fighting/Psychic | +0.57 | -0.94 | 425 | 60 | 75 | 75 | 80 | Maylene |  |
| Jumpluff | Grass/Flying | -0.35 | +0.43 | 450 | 75 | 70 | 85 | 110 | Fantina |  |
| Kricketune | Bug | +0.27 | -0.25 | 444 | 87 | 61 | 61 | 75 | Roark |  |
| Mothim | Bug/Flying | -1.21 | -0.34 | 464 | 80 | 60 | 60 | 76 | Gardenia |  |
| Chimecho | Psychic | +0.42 | +0.01 | 450 | 65 | 70 | 85 | 75 | Gardenia | Levitate (counted) |
| Frosmoth | Ice/Bug | -1.63 | -2.27 | 475 | 70 | 60 | 90 | 65 | Candice |  |
| Delibird | Ice/Flying | -0.17 | +0.53 | 460 | 65 | 60 | 60 | 100 | Candice |  |
| Crustle | Bug/Rock | -1.62 | -0.92 | 485 | 70 | 125 | 75 | 45 | Maylene |  |
| Relicanth | Water/Rock | -1.45 | +0.30 | 485 | 100 | 130 | 65 | 55 | Byron |  |
| Cinccino | Normal | +0.03 | +0.88 | 470 | 75 | 60 | 60 | 115 | Wake |  |
| Lurantis | Grass | -0.26 | -0.36 | 480 | 70 | 90 | 90 | 45 | Maylene |  |
| Ambipom | Normal | +0.03 | +0.88 | 482 | 75 | 66 | 66 | 115 | Fantina |  |

### How each typing's lines fare on average (a dual-typed line counts under both types)

| Type | Lines | Mean index, player's view | Mean index, trainers' view | Mean BST | Mean HP+Def+SpD | Mean Spe |
|---|---|---|---|---|---|---|
| Steel | 16 | +9.10 | +11.07 | 520 | 292 | 57 |
| Ghost | 17 | +5.99 | +7.02 | 510 | 263 | 71 |
| Fairy | 18 | +5.35 | +5.10 | 503 | 272 | 70 |
| Electric | 16 | +4.66 | +4.93 | 489 | 230 | 89 |
| Poison | 17 | +4.62 | +4.86 | 498 | 250 | 81 |
| Dragon | 12 | +3.89 | +3.41 | 550 | 275 | 82 |
| Fire | 19 | +3.34 | +3.46 | 524 | 245 | 88 |
| Fighting | 19 | +3.22 | +2.34 | 512 | 233 | 87 |
| Ground | 18 | +3.01 | +3.18 | 514 | 286 | 55 |
| Flying | 25 | +2.68 | +3.85 | 499 | 245 | 87 |
| Water | 49 | +2.67 | +2.79 | 504 | 265 | 67 |
| Dark | 19 | +2.05 | +2.41 | 512 | 236 | 89 |
| Grass | 25 | +1.07 | +1.19 | 506 | 256 | 70 |
| Bug | 21 | +1.05 | +0.88 | 488 | 232 | 77 |
| Normal | 19 | +0.37 | +1.39 | 497 | 248 | 84 |
| Psychic | 23 | -0.06 | -0.20 | 518 | 263 | 79 |
| Rock | 19 | -0.46 | +0.88 | 508 | 290 | 53 |
| Ice | 16 | -1.32 | -1.17 | 524 | 258 | 82 |

### Every line, by the player's view

| Line | Typing | Index, player's view | Index, trainers' view | BST | HP | Def | SpD | Spe | First owned | Abilities |
|---|---|---|---|---|---|---|---|---|---|---|
| Skarmory | Steel/Flying | +12.84 | +14.93 | 500 | 85 | 140 | 80 | 70 | Galactic | Filter (counted) |
| Klefki | Steel/Fairy | +12.65 | +14.01 | 470 | 57 | 91 | 87 | 75 | Fantina |  |
| Mawile | Steel/Fairy | +12.65 | +14.01 | 440 | 70 | 85 | 75 | 50 | Byron |  |
| Corviknite | Flying/Steel | +11.54 | +14.13 | 495 | 98 | 105 | 85 | 67 | Wake |  |
| Rotom | Electric/Ghost | +11.23 | +12.17 | 525 | 50 | 107 | 107 | 91 | Fantina | Levitate (counted) |
| Hisuian Goodra | Steel/Dragon | +10.17 | +11.59 | 600 | 80 | 100 | 150 | 60 | Byron | Sap Sipper (one slot, +10.7) |
| Gengar | Ghost/Poison | +9.68 | +10.84 | 500 | 60 | 60 | 75 | 110 | Wake | Levitate (counted) |
| Ferrothorn | Grass/Steel | +9.63 | +11.64 | 489 | 74 | 131 | 116 | 20 | Wake |  |
| Magnezone | Electric/Steel | +9.57 | +11.68 | 535 | 70 | 115 | 90 | 60 | Byron | Levitate (one slot, +15.9) |
| Togedemaru | Electric/Steel | +9.57 | +11.68 | 465 | 75 | 73 | 73 | 96 | Byron | Lightning Rod (one slot, +11.0) |
| Empoleon | Water/Steel | +9.37 | +11.67 | 535 | 84 | 93 | 101 | 60 | Maylene |  |
| Scizor | Bug/Steel | +9.26 | +10.88 | 500 | 70 | 100 | 80 | 65 | Maylene |  |
| Lucario | Fighting/Steel | +8.84 | +10.40 | 525 | 70 | 70 | 70 | 90 | Byron |  |
| Steelix | Steel/Ground | +7.75 | +9.73 | 555 | 100 | 200 | 75 | 30 | Gardenia | Solid Rock (one slot, +10.5) |
| Weezing | Poison | +7.68 | +7.54 | 510 | 65 | 120 | 85 | 60 | Maylene | Levitate (counted) |
| Dusknoir | Ghost | +7.47 | +8.38 | 555 | 105 | 135 | 135 | 45 | Candice | Levitate (counted) |
| Mismagius | Ghost | +7.47 | +8.38 | 505 | 60 | 60 | 105 | 105 | Fantina | Levitate (counted) |
| Ceruledge | Fire/Ghost | +7.26 | +8.21 | 525 | 75 | 80 | 100 | 85 | Fantina | Flash Fire (counted) |
| Gastrodon | Water/Ground | +7.06 | +5.89 | 475 | 111 | 68 | 82 | 39 | Fantina | Dry Skin (counted) |
| Annihilape | Fighting/Ghost | +6.68 | +6.44 | 535 | 110 | 80 | 90 | 90 | Byron |  |
| Altaria | Dragon/Fairy | +6.62 | +5.70 | 510 | 75 | 90 | 105 | 80 | Maylene |  |
| Jellicent | Water/Ghost | +6.43 | +7.63 | 480 | 100 | 70 | 105 | 60 | Wake | Water Absorb (one slot, +7.7) |
| Toxicroak | Poison/Fighting | +6.31 | +5.37 | 490 | 83 | 65 | 65 | 85 | Maylene | Dry Skin (counted) |
| Bronzong | Steel/Psychic | +6.22 | +7.85 | 530 | 77 | 116 | 116 | 33 | Fantina | Levitate (one slot, +10.8); Heatproof (one slot, +7.5) |
| Metagross | Steel/Psychic | +6.22 | +7.85 | 605 | 80 | 130 | 90 | 70 | Byron |  |
| Chandelure | Ghost/Fire | +6.11 | +7.27 | 520 | 60 | 90 | 90 | 80 | Wake | Flash Fire (one slot, +7.3) |
| Drapion | Poison/Dark | +5.89 | +6.04 | 500 | 70 | 110 | 75 | 95 | Wake |  |
| Skuntank | Poison/Dark | +5.89 | +6.04 | 499 | 103 | 67 | 61 | 84 | Maylene |  |
| Ninetales | Fire/Fairy | +5.88 | +5.31 | 555 | 85 | 84 | 117 | 95 | Maylene | Magic Guard (counted) |
| Alomomola | Water/Fairy | +5.85 | +5.52 | 470 | 165 | 80 | 45 | 65 | Fantina |  |
| Azumarill | Water/Fairy | +5.85 | +5.52 | 420 | 100 | 80 | 80 | 50 | Gardenia | Sap Sipper (hidden, +9.3) |
| Primarina | Water/Fairy | +5.85 | +5.52 | 530 | 80 | 74 | 116 | 60 | Maylene |  |
| Probopass | Rock/Steel | +5.79 | +8.48 | 555 | 70 | 145 | 150 | 40 | Gardenia | Solid Rock (counted) |
| Galarian Weezing | Poison/Fairy | +5.77 | +5.39 | 490 | 70 | 115 | 105 | 50 | Maylene | Levitate (one slot, +10.4) |
| Galarian Rapidash | Fairy/Fire | +5.54 | +5.16 | 530 | 80 | 85 | 95 | 95 | Gardenia | Pastel Veil (one slot, +6.1) |
| Vikavolt | Bug/Electric | +5.43 | +5.17 | 500 | 77 | 90 | 75 | 43 | Gardenia | Levitate (counted) |
| Emolga | Electric/Flying | +5.40 | +6.22 | 473 | 70 | 70 | 60 | 103 | Gardenia | Motor Drive (hidden, +8.2) |
| Qwilfish | Water/Poison | +5.02 | +5.33 | 500 | 75 | 95 | 65 | 85 | Maylene |  |
| Tentacruel | Water/Poison | +5.02 | +5.33 | 535 | 80 | 65 | 120 | 100 | Fantina |  |
| Toxapex | Poison/Water | +5.02 | +5.33 | 495 | 50 | 152 | 142 | 35 | Maylene | Limber (one slot, +5.5) |
| Quagsire | Water/Ground | +4.79 | +3.80 | 450 | 105 | 85 | 75 | 35 | Gardenia | Water Absorb (one slot, +7.4) |
| Swampert | Water/Ground | +4.79 | +3.80 | 535 | 100 | 90 | 90 | 60 | Maylene |  |
| Whiscash | Water/Ground | +4.79 | +3.80 | 468 | 110 | 73 | 71 | 60 | Fantina |  |
| Cofagrigus | Ghost | +4.60 | +5.63 | 483 | 58 | 145 | 105 | 30 | Maylene |  |
| Poltegeist | Ghost | +4.60 | +5.63 | 508 | 60 | 65 | 114 | 70 | Fantina |  |
| Decidueye | Grass/Ghost | +4.52 | +5.51 | 530 | 78 | 75 | 100 | 70 | Maylene |  |
| Dhelmise | Ghost/Grass | +4.52 | +5.51 | 517 | 70 | 100 | 90 | 40 | Maylene |  |
| Sinistcha | Grass/Ghost | +4.52 | +5.51 | 508 | 71 | 106 | 80 | 70 | Fantina | Heatproof (hidden, +5.8) |
| Talonflame | Fire/Flying | +4.45 | +5.27 | 499 | 78 | 71 | 69 | 126 | Maylene |  |
| Palossand | Ghost/Ground | +4.40 | +5.56 | 480 | 85 | 110 | 75 | 35 | Wake |  |
| Runerigus | Ground/Ghost | +4.40 | +5.56 | 483 | 58 | 145 | 105 | 30 | Candice |  |
| Clefable | Fairy | +4.32 | +3.56 | 488 | 95 | 73 | 90 | 65 | Gardenia | Magic Guard (counted) |
| Froslass | Ice/Ghost | +4.20 | +4.81 | 520 | 80 | 70 | 70 | 110 | Byron | Snow Cloak (counted) |
| Crobat | Poison/Flying | +4.10 | +5.40 | 535 | 85 | 80 | 80 | 130 | Wake |  |
| Florges | Fairy | +4.09 | +3.46 | 552 | 78 | 68 | 154 | 75 | Wake |  |
| Granbull | Fairy | +4.09 | +3.46 | 450 | 90 | 75 | 60 | 45 | Gardenia |  |
| Sylveon | Fairy | +4.09 | +3.46 | 525 | 95 | 65 | 130 | 60 | Fantina |  |
| Kommo-O | Dragon/Fighting | +4.07 | +2.58 | 600 | 75 | 125 | 105 | 85 | Byron | Overcoat (hidden, +4.6) |
| Araquanid | Water/Bug | +4.01 | +3.29 | 454 | 68 | 92 | 132 | 42 | Gardenia | Water Bubble (counted); Water Absorb (hidden, +3.7) |
| Togekiss | Fairy/Flying | +3.94 | +4.64 | 545 | 85 | 95 | 115 | 80 | Wake |  |
| Kingdra | Water/Dragon | +3.82 | +3.00 | 540 | 75 | 95 | 95 | 85 | Wake |  |
| Milotic | Water/Dragon | +3.82 | +3.00 | 540 | 95 | 79 | 125 | 81 | Fantina | Filter (one slot, +4.2) |
| Electivire | Electric/Fighting | +3.80 | +3.16 | 550 | 75 | 67 | 85 | 105 | Volkner |  |
| Pawmot | Electric/Fighting | +3.80 | +3.16 | 490 | 70 | 70 | 60 | 105 | Maylene | Volt Absorb (one slot, +5.2) |
| Lanturn | Water/Electric | +3.78 | +3.63 | 490 | 125 | 68 | 86 | 67 | Fantina | Volt Absorb (one slot, +6.6); Water Absorb (one slot, +5.1) |
| Poliwrath | Water/Fighting | +3.73 | +2.82 | 530 | 90 | 95 | 90 | 90 | Maylene | Water Absorb (one slot, +5.0) |
| Charizard | Fire/Dragon | +3.72 | +3.21 | 535 | 78 | 78 | 85 | 100 | Maylene |  |
| Turtonator | Fire/Dragon | +3.72 | +3.21 | 485 | 60 | 135 | 85 | 36 | Byron |  |
| Gliscor | Ground/Flying | +3.71 | +4.32 | 510 | 75 | 125 | 75 | 95 | Wake | Sand Veil (counted) |
| Drifblim | Ghost/Flying | +3.70 | +6.21 | 498 | 150 | 44 | 54 | 80 | Fantina |  |
| Mantine | Water/Flying | +3.68 | +4.70 | 495 | 85 | 80 | 140 | 70 | Fantina | Water Absorb (one slot, +5.0); Water Veil (hidden, +4.2) |
| Pelipper | Water/Flying | +3.68 | +4.70 | 470 | 60 | 100 | 70 | 65 | Gardenia |  |
| Salazzle | Poison/Fire | +3.67 | +3.80 | 480 | 68 | 60 | 60 | 117 | Fantina |  |
| Bastiodon | Rock/Steel | +3.54 | +6.63 | 515 | 80 | 168 | 138 | 30 | Fantina | Solid Rock (one slot, +5.8) |
| Flygon | Bug/Dragon | +3.51 | +2.31 | 550 | 80 | 80 | 80 | 100 | Byron | Levitate (counted) |
| Hippowdon | Ground | +3.46 | +2.64 | 525 | 108 | 118 | 72 | 47 | Maylene | Thick Fat (counted) |
| Ampharos | Electric/Dragon | +3.45 | +3.39 | 500 | 90 | 75 | 90 | 55 | Fantina |  |
| Jolteon | Electric | +3.42 | +3.16 | 525 | 65 | 60 | 95 | 130 | Maylene | Volt Absorb (counted) |
| Raichu | Electric | +3.42 | +3.16 | 495 | 60 | 60 | 85 | 110 | Maylene | Lightning Rod (counted) |
| Blaziken | Fire/Fighting | +3.39 | +2.64 | 530 | 80 | 70 | 70 | 80 | Maylene |  |
| Houndoom | Dark/Fire | +3.23 | +3.73 | 520 | 75 | 50 | 80 | 105 | Fantina | Flash Fire (one slot, +4.4) |
| Incineroar | Fire/Dark | +3.23 | +3.73 | 530 | 95 | 90 | 90 | 60 | Maylene |  |
| Luxray | Electric/Dark | +3.15 | +3.45 | 523 | 80 | 79 | 79 | 95 | Fantina |  |
| Vaporeon | Water | +3.15 | +3.20 | 525 | 130 | 60 | 95 | 65 | Maylene | Water Absorb (counted) |
| Honchkrow | Dark/Flying | +3.09 | +4.18 | 540 | 100 | 62 | 62 | 91 | Fantina |  |
| Mandibuzz | Dark/Flying | +3.09 | +4.18 | 510 | 110 | 105 | 95 | 80 | Candice | Overcoat (one slot, +3.6) |
| Mr. Mime | Psychic/Fairy | +3.07 | +2.40 | 495 | 65 | 95 | 120 | 90 | Wake | Filter (counted) |
| Clodsire | Poison/Ground | +3.00 | +3.26 | 430 | 130 | 60 | 100 | 20 | Roark | Water Absorb (one slot, +7.3) |
| Nidoking | Poison/Ground | +3.00 | +3.26 | 535 | 81 | 87 | 85 | 85 | Gardenia |  |
| Nidoqueen | Poison/Ground | +3.00 | +3.26 | 535 | 90 | 97 | 95 | 76 | Gardenia |  |
| Crawdaunt | Water/Dark | +2.99 | +3.32 | 468 | 63 | 85 | 55 | 55 | Fantina |  |
| Greninja | Water/Dark | +2.99 | +3.32 | 530 | 72 | 67 | 71 | 122 | Maylene |  |
| Sharpedo | Water/Dark | +2.99 | +3.32 | 460 | 70 | 40 | 40 | 95 | Fantina |  |
| Roserade | Grass/Poison | +2.82 | +2.81 | 505 | 60 | 55 | 105 | 90 | Wake |  |
| Hawlucha | Fighting/Flying | +2.75 | +2.90 | 500 | 78 | 75 | 63 | 118 | Byron | Limber (one slot, +3.3) |
| Galvantula | Bug/Electric | +2.56 | +2.41 | 472 | 70 | 60 | 60 | 108 | Fantina |  |
| Alolan Ninetales | Ice/Fairy | +2.50 | +1.58 | 555 | 79 | 79 | 99 | 100 | Gardenia | Magic Guard (counted) |
| Heracross | Bug/Fighting | +2.43 | +0.86 | 500 | 80 | 75 | 95 | 85 | Gardenia |  |
| Pheromosa | Bug/Fighting | +2.43 | +0.86 | 570 | 71 | 37 | 37 | 151 | Volkner |  |
| Dustox | Bug/Poison | +2.43 | +2.08 | 405 | 60 | 70 | 90 | 65 | Roark |  |
| Grapploct | Fighting | +2.40 | +1.32 | 480 | 80 | 90 | 80 | 42 | Wake | Limber (counted) |
| Volcarona | Bug/Fire | +2.37 | +1.72 | 550 | 85 | 65 | 105 | 100 | HQ |  |
| Masquerain | Bug/Water | +2.37 | +1.84 | 454 | 70 | 62 | 82 | 60 | Gardenia |  |
| Goodra | Dragon | +2.17 | +1.76 | 600 | 90 | 70 | 150 | 80 | Byron | Sap Sipper (one slot, +3.3) |
| Cinderace | Fire | +2.13 | +2.27 | 530 | 80 | 75 | 75 | 119 | Maylene |  |
| Flareon | Fire | +2.13 | +2.27 | 525 | 65 | 60 | 110 | 65 | Maylene | Flash Fire (one slot, +3.3) |
| Magmortar | Fire | +2.13 | +2.27 | 550 | 75 | 67 | 95 | 93 | Fantina |  |
| Rapidash | Fire | +2.13 | +2.27 | 530 | 70 | 75 | 85 | 110 | Wake |  |
| Ludicolo | Water/Grass | +2.12 | +1.29 | 500 | 80 | 80 | 100 | 70 | Maylene |  |
| Minun | Electric | +1.99 | +2.13 | 415 | 65 | 55 | 55 | 105 | Gardenia | Volt Absorb (hidden, +3.4) |
| Pachirisu | Electric | +1.99 | +2.13 | 445 | 60 | 70 | 90 | 95 | Roark | Volt Absorb (hidden, +3.4) |
| Plusle | Electric | +1.99 | +2.13 | 415 | 80 | 95 | 95 | 55 | Gardenia | Lightning Rod (hidden, +3.4) |
| Gardevoir | Psychic/Fairy | +1.91 | +0.99 | 528 | 68 | 65 | 115 | 80 | Fantina | Magic Guard (one slot, +2.1) |
| Hariyama | Fighting | +1.90 | +0.82 | 474 | 144 | 60 | 60 | 50 | Gardenia | Thick Fat (one slot, +4.6) |
| Machamp | Fighting | +1.90 | +0.82 | 505 | 90 | 80 | 85 | 55 | Wake |  |
| Mienshao | Fighting | +1.90 | +0.82 | 510 | 65 | 60 | 60 | 105 | Maylene |  |
| Breloom | Grass/Fighting | +1.86 | +0.71 | 460 | 60 | 80 | 60 | 70 | Gardenia |  |
| Tsareena | Grass/Fighting | +1.86 | +0.71 | 530 | 72 | 98 | 98 | 92 | Gardenia |  |
| Bibarel | Normal/Water | +1.86 | +2.89 | 430 | 79 | 70 | 70 | 71 | Roark |  |
| Blastoise | Water | +1.83 | +2.00 | 535 | 79 | 100 | 105 | 60 | Maylene |  |
| Feraligatr | Water | +1.83 | +2.00 | 540 | 85 | 100 | 85 | 81 | Fantina |  |
| Floatzel | Water | +1.83 | +2.00 | 495 | 85 | 55 | 50 | 115 | Gardenia | Water Veil (hidden, +2.3) |
| Golduck | Water | +1.83 | +2.00 | 500 | 80 | 78 | 80 | 85 | Fantina |  |
| Gorebyss | Water | +1.83 | +2.00 | 485 | 55 | 105 | 75 | 52 | Gardenia |  |
| Huntail | Water | +1.83 | +2.00 | 485 | 55 | 105 | 75 | 52 | Gardenia | Water Veil (hidden, +2.3) |
| Kingler | Water | +1.83 | +2.00 | 500 | 65 | 115 | 65 | 75 | Fantina |  |
| Lumineon | Water | +1.83 | +2.00 | 482 | 69 | 76 | 86 | 91 | Fantina | Water Veil (hidden, +2.3) |
| Manaphy | Water | +1.83 | +2.00 | 600 | 100 | 100 | 100 | 100 | Wake |  |
| Octillery | Water | +1.83 | +2.00 | 524 | 84 | 88 | 88 | 48 | Gardenia |  |
| Politoed | Water | +1.83 | +2.00 | 530 | 90 | 75 | 100 | 90 | Wake | Water Absorb (one slot, +3.1) |
| Seaking | Water | +1.83 | +2.00 | 475 | 85 | 70 | 80 | 70 | Fantina | Water Veil (one slot, +2.3); Lightning Rod (hidden, +6.5) |
| Suicune | Water | +1.83 | +2.00 | 590 | 110 | 115 | 115 | 85 | Candice |  |
| Wailord | Water | +1.83 | +2.00 | 555 | 165 | 65 | 100 | 5 | Wake | Water Veil (one slot, +2.3) |
| Mamoswine | Ice/Ground | +1.78 | +0.84 | 560 | 110 | 80 | 85 | 80 | Maylene | Thick Fat (counted) |
| Chatot | Normal/Flying | +1.74 | +3.50 | 466 | 76 | 45 | 42 | 110 | Maylene |  |
| Noctowl | Normal/Flying | +1.74 | +3.50 | 488 | 100 | 50 | 96 | 70 | Gardenia |  |
| Staraptor | Normal/Flying | +1.74 | +3.50 | 480 | 85 | 70 | 50 | 105 | Maylene |  |
| Toucannon | Normal/Flying | +1.74 | +3.50 | 485 | 80 | 75 | 75 | 60 | Fantina |  |
| Carbink | Rock/Fairy | +1.60 | +2.15 | 500 | 50 | 150 | 150 | 50 | Gardenia |  |
| Magcargo | Fire/Rock | +1.52 | +3.01 | 509 | 70 | 120 | 100 | 30 | Maylene | Solid Rock (counted) |
| Garchomp | Dragon/Ground | +1.46 | +1.51 | 605 | 108 | 95 | 85 | 102 | Byron |  |
| Corsola | Water/Rock | +1.39 | +2.53 | 470 | 65 | 105 | 105 | 35 | Roark | Solid Rock (counted) |
| Carnivine | Grass | +1.23 | +1.06 | 493 | 74 | 72 | 72 | 70 | Fantina | Levitate (counted) |
| Absol | Dark | +1.16 | +1.31 | 530 | 70 | 60 | 60 | 95 | Wake |  |
| Liepard | Dark | +1.16 | +1.31 | 496 | 74 | 60 | 60 | 116 | Gardenia | Limber (one slot, +1.7) |
| Mightyena | Dark | +1.16 | +1.31 | 440 | 70 | 70 | 70 | 70 | Gardenia |  |
| Umbreon | Dark | +1.16 | +1.31 | 525 | 95 | 110 | 130 | 65 | Fantina |  |
| Armarouge | Fire/Psychic | +1.04 | +0.72 | 525 | 85 | 100 | 80 | 75 | Byron | Flash Fire (counted) |
| Mewscarada | Grass/Dark | +0.90 | +0.95 | 530 | 76 | 70 | 70 | 123 | Maylene |  |
| Shiftry | Grass/Dark | +0.90 | +0.95 | 480 | 90 | 60 | 60 | 80 | Gardenia |  |
| Rhyperior | Ground/Rock | +0.78 | +1.82 | 535 | 115 | 130 | 55 | 40 | Byron | Solid Rock (counted) |
| Gallade | Psychic/Fighting | +0.57 | -0.94 | 518 | 68 | 65 | 115 | 80 | Byron |  |
| Medicham | Fighting/Psychic | +0.57 | -0.94 | 425 | 60 | 75 | 75 | 80 | Maylene |  |
| Chimecho | Psychic | +0.42 | +0.01 | 450 | 65 | 70 | 85 | 75 | Gardenia | Levitate (counted) |
| Cresselia | Psychic | +0.42 | +0.01 | 600 | 120 | 120 | 130 | 85 | Volkner | Levitate (counted) |
| Donphan | Ground | +0.28 | +0.43 | 510 | 95 | 130 | 60 | 50 | Gardenia |  |
| Kricketune | Bug | +0.27 | -0.25 | 444 | 87 | 61 | 61 | 75 | Roark |  |
| Glimmora | Rock/Poison | +0.26 | +1.54 | 525 | 83 | 90 | 81 | 86 | Maylene |  |
| Cradily | Rock/Grass | +0.25 | +1.15 | 495 | 86 | 97 | 107 | 43 | Wake | Solid Rock (counted); Storm Drain (hidden, +0.3) |
| Sceptile | Grass/Dragon | +0.12 | -0.33 | 535 | 70 | 65 | 80 | 120 | Maylene |  |
| Ambipom | Normal | +0.03 | +0.88 | 482 | 75 | 66 | 66 | 115 | Fantina |  |
| Blissey | Normal | +0.03 | +0.88 | 540 | 255 | 10 | 135 | 55 | Wake |  |
| Castform | Normal | +0.03 | +0.88 | 510 | 70 | 75 | 75 | 100 | Maylene |  |
| Cinccino | Normal | +0.03 | +0.88 | 470 | 75 | 60 | 60 | 115 | Wake |  |
| Delcatty | Normal | +0.03 | +0.88 | 492 | 70 | 75 | 75 | 112 | Gardenia |  |
| Dubwool | Normal | +0.03 | +0.88 | 490 | 72 | 100 | 90 | 88 | Gardenia | Fluffy (one slot, -1.3) |
| Furret | Normal | +0.03 | +0.88 | 425 | 85 | 64 | 55 | 90 | Roark |  |
| Lickilicky | Normal | +0.03 | +0.88 | 515 | 110 | 95 | 95 | 50 | Maylene |  |
| Lopunny | Normal | +0.03 | +0.88 | 510 | 65 | 84 | 116 | 105 | Gardenia | Limber (hidden, +0.5) |
| Purugly | Normal | +0.03 | +0.88 | 492 | 91 | 74 | 69 | 112 | Maylene | Limber (one slot, +0.5); Thick Fat (one slot, +2.7) |
| Snorlax | Normal | +0.03 | +0.88 | 540 | 160 | 65 | 110 | 30 | Maylene | Immunity (one slot, +0.6); Thick Fat (one slot, +2.7) |
| Delphox | Fire/Psychic | -0.10 | -0.22 | 534 | 75 | 72 | 100 | 104 | Maylene |  |
| Articuno | Ice/Flying | -0.17 | +0.53 | 590 | 90 | 100 | 120 | 85 | Volkner |  |
| Delibird | Ice/Flying | -0.17 | +0.53 | 460 | 65 | 60 | 60 | 100 | Candice |  |
| Arboliva | Grass/Normal | -0.23 | +0.52 | 510 | 78 | 90 | 109 | 39 | Maylene |  |
| Cherrim | Grass | -0.26 | -0.36 | 517 | 70 | 90 | 98 | 85 | Gardenia |  |
| Leafeon | Grass | -0.26 | -0.36 | 525 | 65 | 130 | 65 | 95 | Fantina | Magic Guard (one slot, -0.0) |
| Lurantis | Grass | -0.26 | -0.36 | 480 | 70 | 90 | 90 | 45 | Maylene |  |
| Serperior | Grass | -0.26 | -0.36 | 528 | 75 | 95 | 95 | 113 | Maylene |  |
| Tangrowth | Grass | -0.26 | -0.36 | 535 | 100 | 125 | 90 | 10 | Maylene | Magic Guard (one slot, -0.0) |
| Lunatone | Rock/Psychic | -0.26 | +0.38 | 495 | 90 | 75 | 95 | 70 | Byron | Levitate (counted) |
| Solrock | Rock/Psychic | -0.26 | +0.38 | 495 | 90 | 95 | 75 | 70 | Byron | Levitate (counted) |
| Jumpluff | Grass/Flying | -0.35 | +0.43 | 450 | 75 | 70 | 85 | 110 | Fantina |  |
| Tropius | Grass/Flying | -0.35 | +0.43 | 550 | 105 | 105 | 105 | 51 | Gardenia |  |
| Slowbro | Water/Psychic | -0.62 | -0.74 | 490 | 95 | 110 | 80 | 30 | Maylene |  |
| Slowking | Water/Psychic | -0.62 | -0.74 | 490 | 95 | 80 | 110 | 30 | Wake |  |
| Starmie | Water/Psychic | -0.62 | -0.74 | 540 | 60 | 85 | 100 | 115 | Maylene | Magic Guard (one slot, -0.4) |
| Girafarig | Normal/Psychic | -0.90 | -0.36 | 520 | 85 | 70 | 70 | 85 | Maylene | Sap Sipper (hidden, +1.3) |
| Meloetta | Normal/Psychic | -0.90 | -0.36 | 600 | 100 | 77 | 128 | 90 | Galactic |  |
| Torterra | Grass/Ground | -1.00 | -0.63 | 535 | 95 | 105 | 105 | 56 | Fantina | Thick Fat (one slot, +2.3) |
| Gothitelle | Psychic/Dark | -1.08 | -1.56 | 530 | 80 | 105 | 120 | 65 | Wake |  |
| Beautifly | Bug/Flying | -1.21 | -0.34 | 395 | 60 | 50 | 50 | 65 | Roark |  |
| Mothim | Bug/Flying | -1.21 | -0.34 | 464 | 80 | 60 | 60 | 76 | Gardenia |  |
| Vespiquen | Bug/Flying | -1.21 | -0.34 | 558 | 80 | 102 | 102 | 70 | Gardenia |  |
| Yanmega | Bug/Flying | -1.21 | -0.34 | 515 | 86 | 86 | 56 | 95 | Maylene |  |
| Leavanny | Bug/Grass | -1.23 | -1.85 | 500 | 75 | 80 | 80 | 92 | Fantina | Overcoat (hidden, -1.2) |
| Wormadam | Bug/Grass | -1.23 | -1.85 | 444 | 60 | 85 | 105 | 36 | Gardenia | Overcoat (one slot, -1.2) |
| Weavile | Dark/Ice | -1.24 | -0.91 | 510 | 70 | 65 | 85 | 125 | HQ |  |
| Relicanth | Water/Rock | -1.45 | +0.30 | 485 | 100 | 130 | 65 | 55 | Byron |  |
| Crustle | Bug/Rock | -1.62 | -0.92 | 485 | 70 | 125 | 75 | 45 | Maylene |  |
| Kleavor | Bug/Rock | -1.62 | -0.92 | 500 | 70 | 95 | 70 | 85 | Maylene |  |
| Frosmoth | Ice/Bug | -1.63 | -2.27 | 475 | 70 | 60 | 90 | 65 | Candice |  |
| Tyranitar | Dark/Rock | -1.79 | -0.18 | 600 | 100 | 110 | 100 | 61 | Candice |  |
| Cloyster | Water/Ice | -1.91 | -1.38 | 555 | 50 | 180 | 75 | 70 | Byron | Overcoat (hidden, -1.4) |
| Dewgong | Water/Ice | -1.91 | -1.38 | 500 | 100 | 90 | 100 | 70 | Maylene | Thick Fat (one slot, -0.0) |
| Lapras | Water/Ice | -1.91 | -1.38 | 555 | 130 | 80 | 95 | 60 | Candice |  |
| Walrein | Ice/Water | -1.91 | -1.38 | 545 | 110 | 90 | 90 | 65 | Wake | Filter (one slot, +0.8) |
| Glaceon | Ice | -2.40 | -2.22 | 525 | 65 | 110 | 95 | 65 | Candice | Snow Cloak (counted) |
| Alakazam | Psychic | -2.45 | -2.74 | 490 | 55 | 45 | 85 | 120 | Wake | Magic Guard (hidden, -2.2) |
| Espeon | Psychic | -2.45 | -2.74 | 525 | 65 | 60 | 95 | 110 | Byron |  |
| Abomasnow | Grass/Ice | -2.80 | -3.05 | 494 | 90 | 75 | 85 | 60 | Wake |  |
| Orbeetle | Bug/Psychic | -2.92 | -3.59 | 505 | 60 | 110 | 120 | 90 | Fantina |  |
| Garganacl | Rock | -2.96 | -1.49 | 500 | 100 | 130 | 90 | 35 | Maylene | Purifying Salt (one slot, +0.1) |
| Rampardos | Rock | -2.96 | -1.49 | 500 | 97 | 80 | 70 | 58 | Fantina |  |
| Sudowoodo | Rock | -2.96 | -1.49 | 450 | 85 | 115 | 80 | 30 | Fantina |  |
| Golem | Rock/Ground | -3.18 | -1.56 | 520 | 85 | 140 | 65 | 45 | Wake |  |
| Jynx | Ice/Psychic | -4.35 | -4.76 | 495 | 65 | 57 | 113 | 95 | Fantina | Snow Cloak (counted); Dry Skin (hidden, -3.4) |
| Mr. Rime | Ice/Psychic | -4.35 | -4.76 | 520 | 80 | 75 | 100 | 70 | Wake |  |
| Glalie | Ice/Rock | -4.89 | -3.58 | 520 | 80 | 80 | 80 | 100 | Wake | Solid Rock (one slot, -1.8) |

## How to run it

```
PYTHONPATH=. python3 -m tools.oxide.balance.defensive_index --tables /tmp/tables.md --json /tmp/numbers.json
PYTHONPATH=. python3 -m tools.oxide.balance.test_defensive_index
```

The script is `tools/oxide/balance/defensive_index.py` and its test `tools/oxide/balance/test_defensive_index.py`. The first command prints part 1 and writes this page's tables as Markdown sections and every number as JSON; the tables here were pasted from it.

# Byron: Ian's redraft and a pick for Galvantula's slot

Ian redrafted Byron (Canalave Gym, cap 53) himself on 2026-11-02. This branch, `overseer-byron-ian`, holds his six as he saved it, ready for the full scorer reading he asked for, with Galvantula still in place until he picks its replacement. This page asks that one question and records the checks. No scorer reading was run and the simulator was not touched.

## Summary

Ian's answers of 2026-11-02:

1. The target is 80 to 88 percent won over the three boxes, with no box under 70.
2. His draft goes forward to a full scorer reading.
3. Check HP stays off ("Leave it off"), though Metagross carries Explosion.
4. Empoleon stays, though it is Barry 5's ace for a Scorbunny player.
5. "Propose any galvantula replacements": Galvantula with Sticky Web is Deimos's lead at Pal Park, a few fights earlier in the same split.

His six, flags Basic, Evaluate Attack and Expert:

| Member | Level | Item | Nature | Moves |
|---|---:|---|---|---|
| Metagross (lead) | 50 | Shuca Berry | Naughty | Meteor Mash, Earthquake, Explosion, Stealth Rock |
| Galvantula | 51 | Occa Berry | Hasty | Sticky Web, Thunder, Energy Ball, Bug Buzz |
| Hisuian Goodra (hidden ability, Gooey) | 50 | Leftovers | Brave | Dragon Claw, Earthquake, Muddy Water, Curse |
| Kartana | 51 | Focus Sash | Impish | Brick Break, Smart Strike, Aerial Ace, Swords Dance |
| Empoleon | 52 | Mystic Water | Jolly | Aqua Jet, Flip Turn, Triple Axel, Drill Peck |
| Celesteela (ace) | 53 | Power Herb | Hardy | Flamethrower, Meteor Beam, Air Slash, Flash Cannon |

The question for Ian: which Pokemon takes Galvantula's slot. Each option keeps the other five as he built them.

1. Vikavolt (recommended). Bug and Electric, with Galvantula's own four moves (Thunderbolt for Thunder), Occa Berry, Modest, Levitate. It keeps the whole job and does it better on the cheap checks, but it is slow, and it keeps the Sticky Web that Deimos also leads with.
2. Magnezone. Electric and Steel, Byron's own line (his Magneton in vanilla Platinum): Thunderbolt, Flash Cannon, Thunder Wave, Tri Attack, Occa Berry, Modest, Levitate. The best fit for a Steel gym. It drops the Sticky Web and the Grass hit, so Thunder Wave is its only Speed control and Quagsire goes to Empoleon and Metagross.
3. Togedemaru. Electric and Steel, fast, Sturdy in its hidden slot: Nuzzle, Zing Zap, Fake Out, Electroweb, Occa Berry, Adamant. It keeps Speed control by paralysis and Electroweb, but it hits too softly. The screen reads it the easiest of the four, Galvantula included.

My recommendation is Vikavolt if Ian's objection is to the species, and Magnezone if he also wants Sticky Web gone from Byron. The slot's work is against the Water and Flying walls, and Vikavolt is the only option the AI sends into every one of them, Quagsire and Luxray included.

The counterpiece check, Ian's draft (run `ian-final`) and the Vikavolt pick (run `ian-vikavolt`), against the sixes that beat today's Byron:

| Box (starter) | Ian's draft: won, faints, clean | Very unlucky: won, faints | With Vikavolt: won, faints, clean | Very unlucky: won, faints |
|---|---|---|---|---|
| 1 (Turtwig) | 79, 3.24, 1 | 88, 3.48 | running | running |
| 2 (Scorbunny) | 93, 2.56, 4 | 88, 2.48 | running | running |
| 3 (Piplup) | 88, 2.55, 15 | 60, 4.04 | running | running |
| All | 87, 2.78, 7 | 79, 3.33 | running | running |

The check plays the old reading's sixes only, with no team search, so a number over the target means too easy for certain, and a lower one leaves the decision to the full reading. Box 2 at 93 is over the target on Ian's draft.

Action items for Ian:

1. Pick the slot's member: Vikavolt, Magnezone, Togedemaru, or Galvantula kept. About five minutes.
2. Nothing else: his other answers are applied, and the four off-list moves are on egg lists by the rule.

Next steps. A session swaps the pick into this branch and reruns the legality checks, the lint and the tests, about 20 minutes. Then the Overseer runs the full scorer reading on this branch, two and a half to four hours of machine time.

## The slot's job

Galvantula is the team's answer to the Water and Flying walls. Against every likely answer from goal 3's three boxes at 53 (`byron-redesign.md` has how they are chosen), the trainer AI's own replacement rule, `fightai.replacement`, sends Galvantula in against 10 or 11 answers a box, whichever other member leaves: Manaphy, Corviknight, Quagsire, Whiscash, Kingler, Jellicent, Empoleon, Luxray and the Flying types among them. Its Thunder, Energy Ball and Bug Buzz hit each of those for 51 to 153 percent at the lowest roll, and at 143 Speed it moves first against all but one to four Pokemon of each box. Sticky Web then cuts every switch-in's Speed by a stage. The screen and the calculator do not see that, though it may be much of what the slot gives the rest of the six: after one stage down, Manaphy (118 to 79), Houndoom (124 to 83), Luxray (113 to 75), Delphox (123 to 82) and Rapidash (129 to 86) fall under Metagross (90) and Empoleon (91), and Cinderace (139 to 93) only just stays above them.

In the check, Galvantula made the third most knockouts on box 1 (47 over 75 fights, behind Celesteela and Hisuian Goodra) and the second most on box 3 (40, behind Celesteela), and the fewest on box 2 (19), whose six is mostly Fire and Ground types it hurts little.

What a replacement must keep, then: an Electric hit the Water walls cannot answer, a Grass hit for Quagsire and Whiscash if possible, and Speed control. It must also be off the nearby bosses' teams. Barry 5 fields Staraptor, Primeape, Serperior, Snorlax, Turtonator, Empoleon, Greninja, Torterra and Infernape across his three files, and Riley fields Steelix, Mienshao, Hawlucha, Poliwrath, Kommo-o and Lucario. Thorton's six are Toxapex, Bronzong, Dusclops, Ferrothorn, Turtonator and Guzzlord; Argenta's are Skarmory, Annihilape, Dubwool, Diancie, Meowscarada and Pheromosa. Cyrus 1 brings Swampert, Honchkrow, Porygon-Z, Electivire, Magmortar and Salamence. Phobos and Deimos 2 bring Granbull, Houndoom, Mawile, Feraligatr, Arcanine, Galvantula, Absol, Masquerain, Arbok and Froslass, and Mars 2 Liepard, Crobat, Incineroar, Galarian Zapdos, Mesprit and Purugly. All three options are on none of these teams.

Left out: Forretress has hazards and Thunder Wave but no Electric hit, and is four times weak to Fire, which every box carries. Probopass has Thunderbolt and Thunder Wave, but is four times weak to Ground and Fighting and moves at 40 base Speed. Klefki and Heatran are the old team's, which Ian replaced. Durant is not in Oxide. Magearna, Jirachi and Registeel, weighed by their stats as Ian ruled on 2026-11-01, would be a fifth member of 570 or more, and none answers the Water walls better than Magnezone or Vikavolt.

## The options on the cheap checks

Each option was swapped into Ian's six in memory and checked on the same three boxes: each member's best hit on each likely answer and the answer's best hit back, from the scorer's own calculator rows with Byron's items and the player's left out; who the replacement rule sends in, actually run on a battle built by `perfectline.make_battle`; and the matchup screen. A meeting is "beats" when the member two-hits the answer and takes under half back, or one-hits it moving first; "trades" when both sides take half or more.

| Slot 2 | Speed | Outspeeds, box 1, 2, 3 | Sent in against | Beats, trades, loses | Screen best, box 1, 2, 3 |
|---|---:|---|---|---|---|
| Galvantula (Ian's) | 143 | 81 of 85, 90 of 94, 88 of 89 | 10, 11, 10 | 6/4/0, 6/5/0, 5/5/0 | 16.75, 17.2, 15.5 |
| Vikavolt | 64 | 19, 23, 25 | 10, 11, 10 | 8/2/0, 9/2/0, 9/1/0 | 15.1, 15.4, 13.0 |
| Magnezone | 82 | 36, 44, 48 | 8, 8, 8 | 7/1/0, 6/2/0, 8/0/0 | 15.4, 15.7, 13.0 |
| Togedemaru | 118 | 72, 73, 83 | 8, 8, 8 | 5/3/0, 4/4/0, 5/3/0 | 17.65, 17.35, 16.1 |

Lower on the screen means the player's best six wins its one-on-ones by less. No screen figure turns into a percent won, and the screen counts no Sticky Web and no paralysis.

The counterpiece sixes' members that the slot meets, its hit and the hit back at the lowest roll:

| Answer (box) | Galvantula | Vikavolt | Magnezone | Togedemaru |
|---|---|---|---|---|
| Manaphy (all) | Thunder 71, back 38 | Thunderbolt 89, back 30 | Thunderbolt 82, back 45 | Zing Zap 62, back 50 |
| Corviknight (1) | Thunder 82, back 68 | Thunderbolt 104, back 42 | Thunderbolt 96, back 25 | Zing Zap 59, back 35 |
| Quagsire (1) | Energy Ball 98, back 56 | Energy Ball 149, back 29 | not sent; Tri Attack 30 | not sent |
| Luxray (1) | Bug Buzz 82, back 68 | Bug Buzz 125, back 42 | not sent; Tri Attack 34 | not sent |
| Empoleon (3) | Thunder 76, back 63 | Thunderbolt 98, back 40 | Thunderbolt 90, back 34 | Zing Zap 72, back 47 |

Vikavolt takes Galvantula's place in all but one or two rows of the replacement rule a box, and wins each meeting by more: its Special Attack (145 against 97) and its bulk (77, 90, 75 against 70, 60, 60) outweigh the Speed it gives up, and Levitate turns Quagsire's and Whiscash's Earthquake, 51 to 66 percent into Galvantula, into nothing. The cost is Speed: it moves after Manaphy, Luxray and every Fire type, so it takes a hit before it lays Sticky Web, where Galvantula laid it first.

Magnezone is the strongest pure Electric answer (Corviknight hits it for 25 percent back), and Levitate makes it immune to the Ground moves that hit Galvantula and Metagross for double. It has no Grass or Bug move in its legal palette, so the rule sends Empoleon or Metagross into Quagsire and Hisuian Goodra into Luxray, where Galvantula went before. Thunder Wave is in its four for Speed control; it paralyses one target, where the Web slows every switch-in. Magnezone is also on Cyrus 2's team at Galactic HQ, and on three Workers in Byron's own split; Cyrus 1's answer 4 allowed a species that a later fight uses.

Togedemaru keeps the slot fast and adds Electroweb and Nuzzle, but its one strong hit is Zing Zap, an Electric move, so it has nothing for Quagsire or Luxray and trades with Manaphy where Galvantula beat it. It reads the easiest of the four on the screen.

Speed neighbours, within three points, on each box:

| Slot 2 | Speed | Neighbours |
|---|---:|---|
| Galvantula | 143 | Talonflame (box 1), Greninja and Weavile (box 2) |
| Vikavolt | 64 | Carbink, Lickilicky, Lombre, Donphan, Hippowdon, Hariyama, Octillery |
| Magnezone | 82 | Corviknight, Gothitelle, Nidorino |
| Togedemaru | 118 | Manaphy, Tentacruel, Alolan Ninetales |

Togedemaru's Adamant ties Manaphy at 118; Hasty, freed by Galvantula, would put it at 129.

## The sets

Each set is legal at 51 on both checkers (the OxiDex's lists and the Kaizo checker), the trainer lint finds nothing in a file with it in place, and none repeats an item or a nature of the other five. Occa Berry is Galvantula's own, and every option is weak to Fire.

| Pick | Ability | Item | Nature | Moves |
|---|---|---|---|---|
| Vikavolt | Levitate | Occa Berry | Modest | Sticky Web, Thunderbolt, Energy Ball, Bug Buzz |
| Magnezone | Levitate | Occa Berry | Modest | Thunderbolt, Flash Cannon, Thunder Wave, Tri Attack |
| Togedemaru | Sturdy (hidden) | Occa Berry | Adamant | Nuzzle, Zing Zap, Fake Out, Electroweb |

## What this branch holds and what was checked

Ian's draft is saved into `res/trainers/data/leader_byron.json` through the OxiDex's own save, `tools.oxide.encounters.trainers.save`, which lints the file and records the change in the divergence registry. The file matches his snapshot field for field.

Four of his moves were off-list, and each now sits on its line's first stage's egg list by the egg-list rule (Ian, 2026-10-29), in `learnrewrite.IAN_EGG_MOVES` and in the species files. Kartana takes Smart Strike, which no Oxide list gives it, and Swords Dance, its level 65 move. Piplup takes Flip Turn, which Empoleon learns at 56; Piplup's list is set by hand, so its line in `learnsets_by_hand.txt` says so too. Celesteela takes Air Slash, on no Oxide list for it. Kartana and Celesteela are first stages of their own. The player never reaches an egg list.

The rules: every member holds its own item and has its own nature, with no repeats, and Celesteela, the ace, is at the cap of 53.

Checked on this branch:

| Check | Result |
|---|---|
| The OxiDex's lists, every move at its level | 0 off-list; four before the egg lists (Smart Strike, Swords Dance, Flip Turn, Air Slash) |
| The Kaizo study's checker at 53, with the TMs from before the TM pass | 0 problems; the same four before |
| The trainer lint | nothing found |
| The real packer | packs the file |
| test_b1 | 50 of 50 |
| test_learnrewrite, test_learncheck | 6 of 6, 18 of 18 |
| test_trainers | 44 of 44 |
| `make rom` | builds |
| The gate, `integrate.sh --verify-only` | 53 checks pass with no warning; sync-docs fails, since it refuses to mirror from any branch but `oxide`, by design |

## How the numbers were made

The cheap checks ran in this branch's worktree, on the tree of `origin/oxide` at 9447ef458, with the redesign helper's `shape.py` and its likely answers (`walls.json`, from the run `byron-redesign-study`, seeds 1 to 3 at 53), copied to the job folder `/home/ian/.claude/jobs/382760ce/tmp/byron-ian/` with this page's parties in `shapes.py`; `digest.py` reads their output. None writes to `res/`. Legality comes from the OxiDex's `learnsets.lists` and the Kaizo checker (`oxide.py check 53`, with `OXIDE_OLD_RES` set to an export of `res/` from before the TM pass).

The counterpiece check ran as `ian-final` did: `plcounter read` against the reading `byron-0db1aeaee`, one trial at the reading's dice, target 88, in a tree made by `plcounter tree` from `tree-counter-base-0744cd243` with the Vikavolt file in place (`~/oxide-trials/goal3/tree-counter-byron-ian-vikavolt`). The three boxes ran as three jobs of five processes each, under `tools/oxide/capped`, so they finished sooner; each box's result is in `~/oxide-trials/goal3/counterpiece/byron-0db1aeaee-ian-vikavolt-box<n>.json`.

# Lucas and Dawn 2: a small tune toward 90 to 94 percent won

Lucas and Dawn 2 (Route 207, Fantina's split, honour cap 31) read 100, 92 and 99 percent won on the scorer's three boxes in run `spot-61b9d0391` (at 61b9d0391, before Pursuit went to 60 power). Ian's target when the team was redesigned was 90 to 94, and on 2026-11-02 he chose "Tune it a little". This page proposes the dials from the reading's own evidence, and Ian answered the same day.

## Ian's answers (2026-11-02)

1. Umbreon takes Foul Play for Payback, in all six files. Foul Play's 95 power goes past the redesign's limit of 90 for borrowed attacks, by Ian's choice.
2. Monferno takes Grass Knot for Rock Slide, in the Piplup player's files (`dummy_794` and `dummy_801`) only.
3. The simulator's Foul Play gap is fixed, test first, on its own branch (`overseer-foul-play-fix`), so that a later reading counts the target's Attack and stages.
4. No scorer reading. "its not the end of the world if this is a slightly easy fight." Lucas and Dawn 2 is judged in the playtest (`ingame-checklist.md`, section 3).

Both dials are in the six files on this branch, saved through the OxiDex's own save (the trainer lint and the packer). Both moves are on their species' Oxide lists at the members' levels (Foul Play TM 77 at 29, Grass Knot TM 86 at 31), so no egg list changed. Umbreon's Toxic stays out. The rest of this page is the proposal as Ian read it.

## Summary

**Outcome.** Two members carry the fight and two hardly matter. Scyther is the fight on box 2 (88 of the 133 faints there) but dies on entry on boxes 1 and 3, where the AI's switch rule sends it into a Rock Blast user. Umbreon, the lead, does not do its job of wearing the six down: its one attack is a weak Payback, and the box's Curse users (Grotle on box 1, Onix on box 3) set up on it for free. Monferno, the Piplup version's ace, never matters on box 3 (one faint in 75 fights), because box 3's six is four Water, Rock and Ground walls that none of its moves hits hard. Pursuit's new power reaches box 2 alone in any real way, so it is not enough by itself: I forecast the average moving from about 97 to about 96.

The three dials, ranked by how much each should move the fight:

| Rank | Dial | Files | Boxes it reaches | What changes |
|---|---|---|---|---|
| 1 | Umbreon: Foul Play for Payback | all six | all three, most on 1 and 3 | Umbreon's hit roughly doubles on every slow wall, and in the game Curse and Intimidate no longer blunt it |
| 2 | Monferno: Grass Knot for Rock Slide | `dummy_794`, `801` | box 3 only | Monferno knocks out Onix in one hit and takes 59 to 71 percent of Kingler; the AI now sends it in against Whiscash |
| 3 | Umbreon: Toxic for Confuse Ray | all six | all three, a little each | the chip Toxic gave in stage 4 comes back; Ian swapped it out on 2026-10-22 |

These are forecasts from the calculator, the speed tiers, the replacement rule and the two traced lines, not readings. With Pursuit, dials 1 and 2 together should put boxes 1 and 3 in the middle 90s and box 2 near 90, so the average lands near the target. Box 2 is the one at risk of going under 90, since dial 1 reaches it too.

One finding about the simulator: it scores Foul Play with the user's own Attack stage and ignores the target's, where Oxide's engine does the reverse. On a Grotle at +3 Attack and +3 Defense the engine's Foul Play takes 36 to 43 percent, and the simulator's 14 to 17. So a scorer reading after dial 1 would understate it against every Curse user and every Intimidate holder. The gap is not on the verified gaps list, so a fix needs Ian's approval.

**What Ian decides.**

1. Umbreon's dial. Options: Foul Play for Payback; Toxic for Confuse Ray; both; or neither. Recommended: Foul Play alone. It moves boxes 1 and 3 most, and the AI picks it as often as it picked Payback. Its 95 power is over the redesign's own limit of 90 for borrowed attacks. Toxic is the gentler fallback if he would rather keep that limit.
2. Monferno's Grass Knot for Rock Slide, in the Piplup player's version. Options: yes or no. Recommended: yes. Rock Slide was picked 5 times in 150 probe fights and never in a traced line. Monferno loses its Rock move against Flying types, which Scyther and Pachirisu cover.
3. The simulator's Foul Play gap. Options: approve a fix (the target's Attack and stages, past Unaware, with a test that fails before it); or leave it. Recommended: approve it only if he names a reading in decision 4.
4. Whether the scorer reads the tuned fight. Options: a spot reading of the three boxes; or judge it in the playtest. Recommended: the playtest, since the readings only spot-check now and this tune is small.

**Next steps.** Once Ian answers: the chosen dials go into the files with the trainer lint, the packer, test_b1 and test_trainers, about 30 minutes; the Overseer lands the branch, about 10 minutes; Ian checks Route 207 in game from a save before it, about 15 minutes. A spot reading, if he names one, takes about four hours of machine time (this reading took 150 to 253 minutes a box), plus about an hour for the simulator fix first if dial 1 is taken.

## The reading

| Box (version) | Won | Faints | Clean | Very unlucky won | The scorer's six |
|---|---|---|---|---|---|
| 1 (Turtwig player, Prinplup ace) | 100% | 0.27 | 80% | 100% | Grotle, Luxray, Golbat, Probopass, Quagsire, Cherrim |
| 2 (Scorbunny player, Grotle ace) | 92% | 1.77 | 17% | 80% | Masquerain, Bibarel, Donphan, Naclstack, Tsareena, Leavanny |
| 3 (Piplup player, Monferno ace) | 99% | 0.29 | 84% | 100% | Prinplup, Whiscash, Onix, Kingler, Breloom, Vikavolt |

Which member each of the player's faints was to, over 75 real-odds fights a box:

| Box | Umbreon | Scyther | Lopunny | Pachirisu | Gastrodon | Ace | All |
|---|---|---|---|---|---|---|---|
| 1 | 1 | 10 | 2 | 2 | 2 | 3 | 20 |
| 2 | 4 | 88 | 9 | 10 | 7 | 15 | 133 |
| 3 | 5 | 3 | 7 | 4 | 2 | 1 | 22 |

The traced winning lines show how the player wins. On box 1, Grotle leads, uses Curse three times while Umbreon spends its turns on Reflect, Payback, Confuse Ray and Yawn, and reaches +3 Attack and Defense. After a Bullet Seed, the AI switches Umbreon out to Scyther, which resists Grass four times over, and the boosted Rock Blast knocks Scyther out as it arrives. On box 3, Onix leads, Bulldozes and Curses, the AI switches Umbreon to Scyther (immune to the Ground move), and Rock Blast knocks it out after one Pursuit. On box 2, Scyther does the damage, and the player wins by walling it and Umbreon with Naclstack's Recover.

## Who does their job

The foe's Speeds and the replacement rule, as the simulator builds them. The replacement rule (the trainer AI after a knockout) sends the member whose own types hit the player's Pokemon in front hardest, if it has a super-effective move on it.

| Speed | Lucas or Dawn | Box 1 | Box 2 | Box 3 |
|---|---|---|---|---|
| 84 | Lopunny | | | |
| 74 | Scyther | | | |
| 72 | Pachirisu | | | |
| 70 | Monferno | | | |
| 62 to 68 | | Luxray 68, Golbat 65, Cherrim 62 | Tsareena, Leavanny 66 | |
| 56 | Umbreon | | | Kingler 56 (a tie) |
| 45 to 53 | Prinplup 45 | | Bibarel 53, Masquerain 46 | Onix, Breloom 53, Whiscash 46 |
| 40 or under | Gastrodon 36, Grotle 32 | Probopass 34, Grotle, Quagsire 31 | Donphan 40, Naclstack 31 | Prinplup 40, Vikavolt 36 |

| Member | Its job | Does it? | Why |
|---|---|---|---|
| Umbreon (lead, 56) | wear the six down and cover the members behind it | no, apart from Reflect | Its one attack, Payback, takes 6 to 21 percent of the slow walls (Grotle, Quagsire, Probopass, Onix, Naclstack, Donphan), which it outspeeds, so Payback never doubles there. Confuse Ray and Yawn do not stop a Curse user, so Grotle and Onix set up on it. Its own types hit none of the player's walls hard, so the AI switches it out on a resisted hit, into Scyther. Reflect goes up on the first turn of every traced line. |
| Scyther (74) | punish the Fighting, Bug and Grass types; take the Ground moves aimed at Pachirisu | on box 2, yes; on boxes 1 and 3, no | Wing Attack knocks out Masquerain, Tsareena, Leavanny and Breloom. But every box carries a Rock move, and the AI's switch rule brings Scyther in on a Ground or Grass hit from a Pokemon that also has Rock Blast (Grotle, Onix, Probopass). Onix's and Probopass's Rock Blast take 95 to 123 percent of it, and Grotle's 68 to 82 before Curse. Stage 4 named this risk. |
| Lopunny (84) | the fast threat off the lead | partly | Fake Out fires on each entry and Jump Kick takes Bibarel, Naclstack and Probopass 54 to 77 percent. But it spends long runs of turns on Bounce, its most picked move (six turns of Bounce in a row on box 1), and each charging turn is a free switch. Ian kept its set as it is. |
| Pachirisu (72) | Spark on the Flying and Water types; Seed Bomb on the Ground lead | yes | The rule sends it in on Masquerain, Bibarel, Golbat, Prinplup, Whiscash and Kingler. Spark takes Masquerain 72 to 85 percent and Golbat 61 to 74; Seed Bomb takes Quagsire 55 to 65 and Whiscash 60 to 74. |
| Gastrodon (36) | the Rock and Ground walls; Stealth Rock | yes | The rule sends it in on Probopass, Onix, Naclstack and Luxray. Brine and Earth Power knock out Onix and Naclstack, and Earth Power takes Probopass 74 to 91 and Luxray 82 to 97. Its weakness is Grass: Cherrim, Tsareena, Leavanny and Breloom each knock it out or nearly. |
| Prinplup (box 1 ace, 45) | answer the Water walls | a little | Grass Knot takes Quagsire 80 to 95, and Ice Beam takes Grotle and Golbat over half. Luxray, Golbat and Cherrim all outspeed it, and Luxray's Wild Charge knocks it out. |
| Grotle (box 2 ace, 32) | physical Grass into box 2's answers | yes | Seed Bomb knocks out Bibarel and nearly Naclstack (90 to 110), and Rock Blast takes Masquerain 67 to 81. Fifteen faints, second to Scyther. |
| Monferno (box 3 ace, 70) | the Piplup player's answers | no | Box 3's six is Prinplup, Whiscash, Onix and Kingler beside Breloom and Vikavolt. On the first four its best hit is 19 to 34 percent, and the rule sends it in only on Breloom and Vikavolt, and on Onix once Gastrodon is gone. Rock Slide hits nothing on box 3 that Blaze Kick does not hit harder. |

## Pursuit at 60

Pursuit went from 40 to 60 power in 9e96c3e00, after this reading. Under Technician, Scyther's Pursuit was 60 and is now 90 (Technician raises moves of 60 power or less by half, and 60 still qualifies), and it doubles against a Pokemon switching out.

| Box Pokemon | Pursuit before | Pursuit now | Now, on a switch (about double) |
|---|---|---|---|
| Grotle (box 1) | 21 to 25 | 30 to 36 | 60 to 72 |
| Golbat (box 1) | 24 to 28 | 36 to 42 | 72 to 84 |
| Masquerain (box 2) | 27 to 33 | 39 to 47 | 78 to 94 |
| Bibarel (box 2) | 23 to 28 | 35 to 41 | 70 to 82 |
| Leavanny (box 2) | 22 to 26 | 32 to 38 | 64 to 76 |
| Prinplup (box 3) | 26 to 32 | 40 to 47 | 80 to 94 |
| Kingler (box 3) | 18 to 21 | 26 to 31 | 52 to 62 |

The AI raises Pursuit's score half the time on Scyther's first turn in, and otherwise Wing Attack, Brick Break or Steel Wing hits harder on every Pokemon in the three sixes. So Pursuit matters on the turn Scyther arrives, when the player switches its Grass or Bug type out of Wing Attack's range. That happened in box 2's line, where Pursuit knocked out Tsareena as it left. On boxes 1 and 3 Scyther mostly dies on entry, before Pursuit does anything. My forecast is a point or two off box 2 and almost nothing on boxes 1 and 3, so the average goes from about 97 to about 96. The scorer's player sees Pursuit in its search, so the gain shows as a cost on switching out in front of Scyther, not as a new knockout pattern.

## The dials

### 1. Umbreon: Foul Play for Payback (all six files)

Foul Play is TM 77 and 95 power, and it is on Umbreon's list at 29 today (stage 3 of the redesign found it missing). It hits with the target's Attack, so Timid Umbreon's low Attack no longer matters. Payback doubles only when Umbreon moves last, so the gain is on the slow walls, which are the Pokemon each box leads with or saves for Umbreon.

| Box Pokemon | Payback | Foul Play |
|---|---|---|
| Grotle (box 1) | 17 to 21 | 36 to 43 |
| Quagsire (box 1) | 15 to 17 | 30 to 35 |
| Probopass (box 1) | 6 to 7 | 10 to 12 |
| Golbat (box 1, faster) | 37 to 46 | 39 to 47 |
| Masquerain (box 2) | 21 to 27 | 45 to 54 |
| Bibarel (box 2) | 19 to 23 | 39 to 48 |
| Donphan (box 2) | 10 to 12 | 30 to 36 |
| Naclstack (box 2) | 16 to 20 | 27 to 33 |
| Onix (box 3) | 11 to 15 | 23 to 28 |
| Whiscash (box 3) | 16 to 19 | 30 to 37 |
| Kingler (box 3, a speed tie) | 28 to 33 | 42 to 51 |
| Prinplup (box 3) | 21 to 26 | 44 to 53 |

In the engine, Foul Play uses the target's Attack with its stages, so a Curse user's raised Attack cancels its raised Defense. A Grotle at +3 and +3 still takes 36 to 43 percent, where Payback would take about a third of its usual damage. Masquerain's Intimidate, which cuts Umbreon's own Attack, does not touch it either. That is the answer to the Curse leads that win boxes 1 and 3. The simulator does not model this (the finding in the summary), so a reading would undercount this effect.

Replacement rule: Umbreon now comes back in on box 3's Prinplup, Whiscash and Kingler after Pachirisu faints, in place of Lopunny or Gastrodon, since Foul Play scores highest of the bench's moves there. Nothing else in the trace changes.

The probe (background only, since `probe-ranking.md` shows it misjudges this range): the AI picked Foul Play 314 to 489 times in 150 fights a box, about as often as it had picked Payback, and the player's Pokemon knocked out while Umbreon was in rose from 72, 22 and 44 to 104, 53 and 97 on boxes 1, 2 and 3.

The cost is box 2: Masquerain, Bibarel and Donphan take twice what they did, and box 2 is already at 92.

### 2. Monferno: Grass Knot for Rock Slide (the Piplup player's files, `dummy_794` and `801`)

Grass Knot is TM 86, on Monferno's list at 31; its power is set by the target's weight. Against box 3:

| Box 3 Pokemon | Monferno's best hit today | Grass Knot |
|---|---|---|
| Onix | Mach Punch 23 to 30 | 213 to 253 (Monferno moves first, 70 against 53) |
| Kingler | Zen Headbutt 19 to 22 | 59 to 71 |
| Whiscash | Zen Headbutt 19 to 24 | 42 to 53 |
| Prinplup | Zen Headbutt 28 to 34 | 26 to 33 |
| Vikavolt | Blaze Kick 77 to 92 (Rock Slide 39 to 47) | 9 to 11 |

Replacement rule: Monferno now comes in on Whiscash after any other member faints, and on Prinplup and Kingler after Pachirisu faints, where before it came in only on Breloom, Vikavolt, and Onix once Gastrodon was gone. Whiscash's Water Pulse takes 67 to 80 percent of Monferno and Kingler's Aqua Jet 62 to 76 with priority, so these are trades, not free knockouts, but each leaves a wall low for Pachirisu's Seed Bomb or Lopunny's Quick Attack.

The probe: Monferno picked Grass Knot 288 times in 150 fights, the player's Pokemon knocked out while it was in rose from 106 to 153, and the greedy player's wins fell from 12 to 3 of 150.

What it gives up: Rock Slide was Monferno's move for the Flying and Bug types, and a real Piplup player's box holds Golbat, Corvisquire, Vullaby and Combee. Scyther's Brick Break and Pachirisu's Spark still cover the Flying types. It does not reach boxes 1 and 2.

### 3. Umbreon: Toxic for Confuse Ray (all six files)

This reverses Ian's swap of 2026-10-22. Toxic chips every wall that stays in, which is what a non-lead Lopunny's Fake Out and Quick Attack need, and with Yawn it pushes a Curse user out before it sweeps. Golbat and Probopass (box 1) are immune by type, and Naclstack (box 2) by Purifying Salt. The probe: the AI picked Toxic 54 to 57 times in 150 fights (Confuse Ray had 83 to 132), and the knockouts while Umbreon was in rose from 72, 22 and 44 to 93, 40 and 53. That is a smaller effect than Foul Play on every box, but the simulator models it fully, and it is gentler on box 2.

Toxic and Foul Play can go together (Yawn, Toxic, Reflect, Foul Play), at the cost of Confuse Ray and Payback both.

### Considered and set aside

Lopunny's Bounce for Ice Punch would take Golbat 61 to 74 percent where Bounce takes 28 to 34, and would end the free switches. But it would ease box 2, where Bounce knocks out Tsareena and Leavanny and Ice Punch takes 49 to 67, and Ian kept Lopunny's set as it is. Scyther's Rock weakness has no one-move or one-item fix: Rock Blast hits several times, so a Charti Berry or a Focus Sash stops only the first hit, and Umbreon cannot be kept in against both Grotle and Onix by one super-effective move.

If box 1 still reads over 94 after dial 1, its own ace, Prinplup, is the place to look next.

## How the numbers were made

Damage is the calculator's own runner, through the rows `plscore.prepare` builds for the fight, on the box each result rebuilt from the run's own history (`plgoal3.setup`, run `spot-61b9d0391`), as a share of the defender's HP, lowest roll to highest. The reading's tree (`~/oxide-trials/goal3/tree-cyrus-1`) and this branch's gave the same boxes and the same numbers but Pursuit's. Speeds are those a battle gives each side. The replacement trace is `fightai.replacement`, the engine's rule, with each of the six in front and each member fainted. The dials were put into the trainer files in memory only. The probe is the Mars 2 check's greedy player, 150 rough fights on each box against the reading's own six; its win and faint numbers are background only. Oxide's Foul Play rule is the calculator's Oxide profile, which follows battle_lib.c. The simulator's gap was checked by scoring Umbreon's Foul Play on box 1's Grotle with Grotle at +3 Attack and Defense (13 to 16 HP of 92) and with Umbreon at -1 Attack (22 to 26), against 33 to 40 HP unboosted.

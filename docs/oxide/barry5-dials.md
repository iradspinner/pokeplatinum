# Barry 5: dials in checked stages

Barry 5 (Canalave's bridge, Byron's split, honour cap 50) read too easy on the scorer: 99, 100 and 93 percent won on the three boxes (run `barry-5-38981fc80`), against a boss ceiling of 95. Ian asked for "Dials in checked stages" on 2026-11-02. This page is stages 1 and 2 for each of the three versions, and the counterpiece check of the top dials against the sixes the reading chose. No trainer file changes until Ian picks. No scorer reading was run, and the simulator was not touched.

## Summary

No dial brings a version under the ceiling on the check. Every one tested reads too easy for certain: the reading's own six still wins 97 to 100 percent of its fights at real odds. The Scorbunny version stays at 100 percent won with any one dial and with two dials together, though the player's faints rise from 0.05 a fight to as much as 1.11. The one dial that moved the win rate at real odds is Snorlax's Immunity, which took the Turtwig version from 99 to 97 percent won and its faints from 0.95 to 1.49. Snorlax is shared, so that dial changes every version. On the Scorbunny version's box it read 100 percent won, with faints up from 0.05 to 0.65 and Snorlax making 25 knockouts where it made none. The Piplup version already reads 93 percent won, under the ceiling, and needs no dial.

Why the versions are easy, in one line each. The Scorbunny version loses to Glimmora, whose Toxic Debris turns Staraptor's own Close Combat into poison on Barry's back line, and to Heracross, which takes Empoleon in one hit before it moves. The Turtwig version leans on Greninja for most of its knockouts while Infernape loses its race with Corviknight, and the same Glimmora poisons it. In the Piplup version the members do their jobs, and Torterra is the one that underdelivers.

The counterpiece rows, each dial against the six the reading chose on its own box (75 fights at real odds and 25 very unlucky ones):

| Version (box) | Dial | Won | Faints | Clean | Very unlucky: won, faints |
|---|---|---:|---:|---:|---|
| Scorbunny (2) | none, the reading | 100 | 0.05 | 96 | 100, 0.08 |
| Scorbunny (2) | S1, Empoleon takes the Chople Berry, Snorlax the Sitrus Berry | 100 | 0.55 | 49 | 100, 0.68 |
| Scorbunny (2) | S2, Turtonator's Earthquake for Iron Defense | 100 | 0.19 | 85 | 100, 0.28 |
| Scorbunny (2) | S3, Snorlax's Immunity for Thick Fat | 100 | 0.65 | 43 | 100, 0.72 |
| Scorbunny (2) | S4, Greninja in Turtonator's slot | 100 | 0.59 | 52 | 96, 1.48 |
| Scorbunny (2) | S1 and S4 together | 100 | 1.11 | 1 | 100, 1.48 |
| Turtwig (1) | none, the reading | 99 | 0.95 | 32 | 100, 1.24 |
| Turtwig (1) | T1, Infernape's Charcoal for the Muscle Band | 100 | 0.95 | 39 | 100, 1.80 |
| Turtwig (1) | T2, Snorlax's Immunity for Thick Fat | 97 | 1.49 | 24 | 88, 2.40 |
| Piplup (3) | none, the reading | 93 | 2.23 | 5 | 92, 2.80 |

Ian's decisions:

1. The Scorbunny version: a stage 3 redesign of it from Barry's pool, with S1 (Empoleon takes the Chople Berry) and Snorlax's Immunity kept as its start (recommended), or take S1 and S4 (Greninja in Turtonator's slot) now and stop there, or accept it as the box difference Ian named on 2026-11-01?
2. Snorlax's Immunity in place of Thick Fat, in all three files: take it (recommended; it is the only dial that moved a win rate, and it costs Snorlax its Fire and Ice resistance), or leave Thick Fat?
3. The Turtwig version beyond Immunity: no other dial (recommended; the Charcoal read worse, with Infernape's knockouts falling from 8 to 5), or fold it into the stage 3 redesign with the Scorbunny version?
4. The Piplup version: keep it as it is at 93 percent (recommended), or give its Turtonator Earthquake so the two Turtonator sets match (no change on the cheap checks)?

Next steps, once Ian answers:

| Step | Who | Time |
|---|---|---|
| Stage 3 for the Scorbunny version: two or three whole-team candidates from the pool, on the cheap checks | a helper | one to two hours |
| The counterpiece check of each candidate on box 2 | a helper | 25 minutes a candidate, two at a time |
| Write the picked dials into the trainer files and land them | a helper, then the Overseer | an hour |
| A full reading of the changed versions, only if Ian names it | the Overseer | two and a half to four hours |

## Stage 1: the evidence and the diagnosis

Each version meets one box: box 1 the Turtwig player's file, box 2 the Scorbunny player's, box 3 the Piplup player's. The reading's own files give what each member did: the knockouts it made over the 75 fights at real odds, and the line the scorer traced for one fight. The calculator figures below are the lowest and highest roll as a percent of the target's HP, with Barry's items in and the player's item left out.

| Barry's member | Box 1 (Turtwig file) | Box 2 (Scorbunny file) | Box 3 (Piplup file) |
|---|---:|---:|---:|
| Staraptor (lead) | 0 | 2 | 9 |
| Primeape | 11 | 0 | 38 |
| First partner | Serperior 4 | Serperior 0 | Greninja 59 |
| Snorlax | 7 | 0 | 40 |
| Second partner | Greninja 41 | Turtonator 0 | Turtonator 7 |
| Ace | Infernape 8 | Empoleon 2 | Torterra 14 |
| All, per fight | 0.95 | 0.05 | 2.23 |

The player's faints, by the Pokemon that fell, over the same 75 fights:

| Box | Six | Faints |
|---|---|---|
| 1 | Whiscash, Luxray, Corviknight, Crobat, Glimmora, Grapploct | Luxray 38, Crobat 9, Grapploct 8, Glimmora 8, Whiscash 5, Corviknight 3 |
| 2 | Cinderace (Scorbunny held to 45), Whiscash, Staraptor, Glimmora, Heracross, Manaphy | Heracross 2, Cinderace 1, Manaphy 1 |
| 3 | Crobat (Zubat held to 41), Breloom, Bastiodon, Leavanny, Hippowdon, Araquanid | Araquanid 41, Leavanny 33, Crobat 31, Breloom 26, Bastiodon 21, Hippowdon 15 |

### The Scorbunny version (box 2): no member does its job

Barry's six made four knockouts in 75 fights. The traced line shows how the six takes him apart, and the calculator says the same line works every time.

Glimmora is the answer to Staraptor. Its Power Gem takes 124 to 148 percent of Staraptor, and Staraptor's best hit back is Close Combat at 37 to 45. Each physical hit on Glimmora lays a layer of Toxic Spikes on Barry's side (Toxic Debris), so Staraptor's own attack poisons his back line. Every member but Staraptor and Empoleon is poisoned as it comes in, and in the traced line Turtonator, Snorlax, Primeape and Serperior all arrive poisoned. Box 1's line does the same with two hits, which makes the poison bad poison.

The AI's replacement rule then sends Empoleon into Glimmora, for its Earthquake (144 to 170 percent). The player switches Heracross into the Earthquake. Heracross moves first (97 against Empoleon's 80) and its Close Combat with the Fist Plate takes 116 to 137 percent of Empoleon, so the ace falls in one hit before it can Swords Dance or Drill Peck. Drill Peck would take 138 to 163 percent of Heracross, so the whole matchup turns on who survives the first hit.

The rest fold. Serperior is drawn in by Whiscash and Manaphy, whom it hits hard, but Cinderace's Flare Blitz takes 108 to 129 percent of it and Cinderace is faster (131 against 128). Turtonator and Snorlax arrive poisoned and spend turns on Iron Defense and Curse. Primeape hits none of the six for more than 45 percent but Staraptor (Ice Punch, 67 to 78), and Staraptor is faster (117 against 108) and takes it in one Brave Bird.

The six without held-back versions (Cinderace, Crobat, Tentacruel, Glimmora, Heracross, Araquanid) also read 100 percent, so the version is easy for this box's catches, not for one lucky six.

### The Turtwig version (box 1): Greninja works, the ace does not

Greninja made 41 of the 71 knockouts; it is drawn into Glimmora and Crobat, which its Water Shuriken and Ice Beam hit hard. Water Shuriken is special in Oxide, so it lays no Toxic Spikes. Infernape, the ace, made 8. Corviknight is in all 20 of the screen's top sixes and draws Infernape from every slot but Infernape's own. Infernape moves first (140 against 79), but its Fire Punch with the Muscle Band takes only 90 to 106 percent, so Corviknight often survives and its Brave Bird takes 110 to 130 percent back. That is the narrow loss the lead test found in `barry5-riley.md`. Crobat is also two points faster than Infernape (142 against 140), and its Dual Wingbeat takes 78 to 94 percent. Glimmora's Toxic Debris hits this version too: Staraptor's Brave Bird and Close Combat into it put bad poison on everything that follows.

### The Piplup version (box 3): under the ceiling already

Box 3 has no Glimmora, and the version reads 93 percent won with 2.23 faints, under the ceiling of 95. Greninja (59), Snorlax (40) and Primeape (38) do their jobs. Torterra, the ace, made 14. Bastiodon draws it second, which is the right call (Headlong Rush, 104 to 122 percent), but the player switches Breloom into it, and Torterra has no hit for Breloom (Wood Hammer 37 to 44). Breloom's Spore and Hippowdon's Yawn then put Turtonator to sleep while it raises its Defence to +6. Turtonator's job against this box is Breloom and Leavanny (Shell Trap takes 188 to 315 percent), but the replacement rule sends it against them only when Staraptor is the member that fell; from every other slot Staraptor goes in.

## Stage 2: the dials

A dial changes one member or one set. Each was swapped into the version's file in memory and checked on its own box: the calculator, the speed tiers, the AI's replacement rule (`fightai.replacement`, run on a battle built by `perfectline.make_battle`) and the matchup screen, where a lower best-six score means the player's best six wins its one-on-ones by less. Every move named is legal at its level on the OxiDex's lists, and no dial repeats an item or a nature in its team.

The Speeds that matter, from the simulator's own build of each member:

| Box | Barry's members | The six |
|---|---|---|
| 1 | Infernape 140, Greninja 137, Serperior 128, Staraptor 120, Primeape 108, Snorlax 44 | Crobat 142, Luxray 107, Glimmora 98, Corviknight 79, Whiscash 72, Grapploct 54 |
| 2 | Serperior 128, Staraptor 120, Primeape 108, Empoleon 80, Turtonator 54, Snorlax 44 | Cinderace 131, Staraptor 117, Manaphy 112, Glimmora 98, Heracross 97, Whiscash 72 |
| 3 | Greninja 137, Staraptor 120, Primeape 108, Torterra 76, Turtonator 54, Snorlax 44 | Crobat 142, Leavanny 104, Breloom 82, Hippowdon 59, Araquanid 54, Bastiodon 42 |

### The Scorbunny version, first

S1, Empoleon takes Snorlax's Chople Berry and Snorlax takes Empoleon's Sitrus Berry. It is one item trade, though it touches two members, because no other Berry answers a Fighting hit and Snorlax holds the only Chople. Heracross's Close Combat on Empoleon falls from 116 to 137 percent to 58 to 68, so Empoleon lives through the hit that ended it in the traced line, and its Drill Peck takes 138 to 163 percent of Heracross back. Staraptor's Close Combat on it falls from 75 to 89 to 37 to 44, and Manaphy's Aura Sphere from 35 to 42 to 17 to 21. The cost is Snorlax: Heracross's Close Combat on it rises from 48 to 57 percent to 97 to 115. The replacement rule never sends Snorlax into Heracross (Staraptor goes in from five slots, Turtonator from the sixth), so Snorlax meets it only when the player switches Heracross in. Speeds do not change. The screen's best six falls from 15.70 to 15.15, the largest move of any dial here, and Heracross rises from 3 to 10 of the top 20 sixes, as the screen now needs it against Empoleon.

S2, Turtonator's Iron Defense becomes Earthquake (TM 26). Its Earthquake takes 90 to 106 percent of Glimmora (Shell Trap took 30 to 36), 53 to 63 of Cinderace and 56 to 68 of Rapidash. Glimmora still moves first (98 against 54) and its Power Gem still takes 98 to 116 percent of Turtonator, so the Earthquake lands on Glimmora only when Turtonator survives a high roll or comes in on another hit. The replacement rule sends Turtonator into Glimmora only when Empoleon is the member that fell. Its gain is the turns Iron Defense wasted against a poisoned clock. The screen moves from 15.70 to 15.55, and Glimmora falls from 14 to 8 of the top 20 sixes. The cheap probe of `barry5-riley.md` read the same dial at 75 and 86 wins of 150, from 105 and 97.

S3, Snorlax's Thick Fat becomes Immunity, its first ability. It blocks the Toxic Debris poison on the one member that sets up longest, but Snorlax is shared, so it changes all three versions. The cost is Thick Fat's halving of Fire and Ice: Cinderace's best hit on Snorlax becomes Flare Blitz at 45 to 53 percent, and Rapidash's Flare Blitz rises from 25 to 30 to 50 to 59. The screen counts no poison, so it reads no change (15.70). On the check it is the best single dial for the Scorbunny version by faints (0.65), and the best of all on the Turtwig version (T2).

S4, Greninja takes Turtonator's slot, with the Turtwig version's set (Expert Belt, Rash, Water Shuriken, Dark Pulse, Ice Beam, Gunk Shot). It was added after S1 and S2 both read 100 on the check. It answers the three Pokemon that beat this version, and it moves first against all three: Water Shuriken takes 102 to 122 percent of Cinderace (137 against 131) and 90 to 114 of Glimmora (against 98), and Ice Beam takes 107 to 126 of Staraptor (against 117). Water Shuriken is special, so it lays no Toxic Spikes from Glimmora. The replacement rule sends it in against Cinderace, Rotom, Crobat and Rapidash from five slots of six, and against Glimmora when Empoleon is the member that fell. Its weak point is Heracross, whose Close Combat takes 156 to 185 percent of it while Gunk Shot does 38 to 44. The screen's best six falls from 15.70 to 15.30, and Empoleon itself rises to 17 of the top 20 sixes, as the box's own Empoleon becomes the screen's answer to two Water types. The cost is the version's shape: Barry's pool gives every version one Fire, one Water and one Grass member, as vanilla Platinum's Barry did, and this one would carry two Water types (Empoleon and Greninja) and no Fire.

### The Turtwig version

T1, Infernape's Muscle Band becomes a Charcoal. Fire Punch on Corviknight rises from 90 to 106 percent to 99 to 117, so the one-hit knockout lands on nearly every roll, and Corviknight, in all 20 top sixes, draws Infernape from five slots of six. This is the narrow loss of the lead test. The cost is every non-Fire hit: Drain Punch on Luxray falls from 103 to 122 percent to 93 to 111, Thunder Punch on Crobat from 82 to 98 to 76 to 90, and Thunder Punch on Tentacruel from 102 to 121 to 93 to 111. Infernape stays at 140, two under Crobat. The screen's best six is unchanged at 15.15, and Glimmora and Grapploct rise in the top 20 (14 to 17, 13 to 16).

T2, Snorlax's Immunity, as S3. Box 1's traced line put bad poison on everything after Staraptor, from Staraptor's two hits on Glimmora.

### The Piplup version

P0 is to keep it: it reads 93, under the ceiling, and the cheap checks found no dial worth its cost there. Two dials were checked in case Ian wants this version harder or the two Turtonator files kept alike. P1, Earthquake for Iron Defense, as S2: no calculator row against box 3's six changes, since Body Press already hits Bastiodon harder than Earthquake would (Turtonator's Defence is higher than its Attack, and Solid Rock cuts both), and the screen stays at 18.35. P2, Dragon Pulse (its level 43 move) for Iron Defense: it hits Hippowdon for 33 to 40 percent, against Shell Trap's 29 to 36, and the screen falls from 18.35 to 18.05. A Lum Berry on Torterra for Breloom's Spore and Hippowdon's Yawn was also tried, and the screen rose from 18.35 to 19.0 without the Coba Berry (Crobat's Dual Wingbeat rises to 44 to 56 percent), so it is not offered.

## The counterpiece check

The check plays each dial against the six the reading chose on the dial's own box, with the scorer's own planner on the reading's final stage: 75 fights at real odds on the reading's dice and 25 very unlucky ones, with no team search. Its logic is one-sided. A full search could only find the player a stronger six than the old one, so a result over the target of 95, or one where the old six still wins about as often as it beat the old team, is too easy for certain. A result under it says only that a full reading decides.

The rows are in the summary's table. The verdict for every row is "too easy": either the old six wins about as often as it beat the old team, or the rate is over 95.

What each run says about the members. With the Chople Berry (S1), Empoleon made 29 knockouts where it made 2, and Glimmora fell in 22 fights, but the six still won all 75. With Earthquake (S2), Turtonator made none and Empoleon 9. With Greninja in the slot (S4), knockouts spread over the whole team (Snorlax 11, Primeape 9, Staraptor 8, Greninja 8, Serperior 6), and the very unlucky fights lost one of 25. With the Charcoal (T1), Infernape made 5 knockouts where it made 8, and Greninja carried the team as before (44); the Fire Punch on Corviknight did not make up for the hits it weakened. With Snorlax's Immunity (T2), the knockouts rose from 71 to 112 over the 75 fights (Greninja 50, Staraptor 20, Infernape 15, Primeape 11, Snorlax 11, Serperior 5), Grapploct fell in 30 fights where it fell in 8, and the very unlucky fights lost 3 of 25. The check calls it too easy all the same, since 97 is over the target and within the scorer's tolerance of the old 99. With Immunity on the Scorbunny version (S3), Snorlax made 25 knockouts where it made none and Empoleon 17, but Cinderace, Staraptor and Heracross still took the fight every time. With S1 and S4 together, Empoleon made 69 knockouts, 66 of them on Glimmora, which the player now spends in nearly every fight and still wins.

## Each box's catches, and the six that played

Each version is checked against one box only: goal 3's run whose player chose the matching starter, its catches rolled from the encounter tables up to Barry 5 and stood at his cap of 50. The reading's six may hold a held-back version of a catch, kept unevolved to a level, which the label names. `plgoal3 --run barry-5-38981fc80 --box barry_5 <seed>` prints each box in full.

| Box | Catches | The six that played, with its moves | Reading |
|---|---|---|---|
| 1 (Turtwig file) | Torterra, Whiscash, Luxray, Staraptor, Bibarel, Dustox, Nidorino, Pawmo, Corviknight, Vullaby, Crobat, Talonflame, Probopass, Seaking, Quagsire, Kingler, Tentacruel, Cherrim, Sharpedo, Plusle, Leavanny, Lombre, Alolan Ninetales, Abomasnow, Vespiquen, Gengar, Togetic, Bastiodon, Garganacl, Sylveon, Carbink, Lurantis, Granbull, Glimmora, Crawdaunt, Dhelmise, Floette, Lickilicky, Golem, Arboliva, Drifblim, Jynx, Crustle, Palossand, Altaria, Grapploct, Tangrowth, Seadra, Manaphy, Pachirisu, Jellicent, Houndoom, Magmar, Cinderace, Lumineon | Whiscash (Earthquake, Icy Wind, Zen Headbutt, Aqua Tail), Luxray (Wild Charge, Fire Fang, Crunch, Double Kick), Corviknight (Brave Bird, Taunt, Iron Head, Revenge), Crobat (Dual Wingbeat, Poison Fang, Leech Life, Steel Wing), Glimmora (Sludge Wave, Ancient Power, Flash Cannon, Mud Shot), Grapploct (Superpower, Taunt, Body Slam, Skitter Smack) | 99 percent won, 0.95 faints, 32 percent clean |
| 2 (Scorbunny file) | Cinderace, Whiscash, Staraptor, Masquerain, Lombre, Bibarel, Orbeetle, Liepard, Nidorino, Vullaby, Crobat, Rapidash, Donphan, Seaking, Garganacl, Lumineon, Tentacruel, Vespiquen, Arboliva, Tsareena, Leavanny, Primarina, Alolan Ninetales, Bronzong, Nuzleaf, Rotom, Togetic, Bastiodon, Onix, Sylveon, Glimmora, Heracross, Granbull, Glalie, Pachirisu, Gothitelle, Floette, Murkrow, Golem, Weavile, Mienshao, Rhydon, Hippowdon, Crustle, Absol, Araquanid, Quagsire, Greninja, Seadra, Manaphy, Pikachu, Jellicent, Gliscor, Delphox, Empoleon, Gastrodon | Cinderace, Scorbunny held to 45 (Flare Blitz, Super Fang, Jump Kick, Taunt), Whiscash (Earthquake, Icy Wind, Zen Headbutt, Aqua Tail), Staraptor (Brave Bird, Close Combat, Tailwind, Take Down), Glimmora (Sludge Wave, Power Gem, Mud Shot, Flash Cannon), Heracross (Close Combat, Pin Missile, Bulk Up, Take Down), Manaphy (Aura Sphere, Bubble Beam, Icy Wind, Acid Armor) | 100 percent won, 0.05 faints, 96 percent clean |
| 3 (Piplup file) | Empoleon, Seaking, Corviknight, Orbeetle, Dubwool, Bibarel, Nidorino, Machamp, Whiscash, Vullaby, Crobat, Hariyama, Onix, Roselia, Golem, Kingler, Tentacruel, Pachirisu, Pawmo, Vespiquen, Breloom, Lombre, Mothim, Carbink, Vikavolt, Rotom, Togetic, Bastiodon, Salazzle, Leafeon, Crustle, Leavanny, Granbull, Bronzong, Gothitelle, Sinistea, Floette, Happiny, Cofagrigus, Delphox, Drifblim, Masquerain, Hippowdon, Palossand, Absol, Araquanid, Quagsire, Jellicent, Arboliva, Manaphy, Skitty, Milotic, Lucario, Crawdaunt, Cinderace, Octillery | Crobat, Zubat held to 41 (Dual Wingbeat, Leech Life, Poison Fang, Air Slash), Breloom (Force Palm, Bullet Seed, Bulldoze, Spore), Bastiodon (Rock Blast, Hard Press, Zen Headbutt, Taunt), Leavanny (Leaf Blade, X-Scissor, Throat Chop, Sticky Web), Hippowdon (Earthquake, Ice Fang, Yawn, Double-Edge), Araquanid (Dive, Lunge, Sticky Web, Headbutt) | 93 percent won, 2.23 faints, 5 percent clean |

The items the scorer gave each six from the run's stock: box 1 Crobat Poison Barb, Glimmora Rock Incense, Luxray Black Glasses, Corviknight Metal Coat, Grapploct Fist Plate, Whiscash Mystic Water; box 2 Manaphy Mystic Water, Cinderace Sitrus Berry, Glimmora Poison Barb, Heracross Fist Plate, Staraptor Silk Scarf, Whiscash Sitrus Berry; box 3 Crobat Poison Barb, Hippowdon Sitrus Berry, Bastiodon Rock Incense, Leavanny Miracle Seed, Breloom Fist Plate, Araquanid Mystic Water. The reading also played each box's best six without held-back versions: box 2's (Cinderace, Crobat, Tentacruel, Glimmora, Heracross, Araquanid) read 100 percent won, and box 3's (Corviknight, Dubwool, Hariyama, Gothitelle, Hippowdon, Araquanid) 99 percent with 1.35 faints.

## How the numbers were made

The cheap checks are `dial.py` and `shapes.py` in the job folder `/home/ian/.claude/jobs/barry5-dials/`, run from inside `~/oxide-trials/goal3/tree-barry5`, the reading's own tree at 38981fc80, since the boxes on `oxide` changed today when the Elekid gift was removed. Each box is rebuilt by `plgoal3.setup` with the reading's run name, the reading's six is given its moves, and the candidate party is swapped in memory; none writes to `res/`. `diff.py` prints what a dial changes against the base. The counterpiece check is `plcounter read` from branch `overseer-counterpiece`, one trial at the reading's dice, target 95, in a tree made by `plcounter tree` from `tree-barry5` with the candidate's file (`~/oxide-trials/goal3/tree-barry5-<dial>`); each run's result is in `~/oxide-trials/goal3/counterpiece/barry-5-38981fc80-<dial>-box<n>.json`. Runs went two at a time under `tools/oxide/capped`, five processes each, beside Byron's reading, each started with 10 GB or more available on `free -g` (the Overseer's measure from the third run on; the first two waited for 10 GB in the free column). A box 2 run took 24 to 27 minutes and a box 1 run 27 to 31.

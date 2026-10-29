# Fantina's redesign: the evidence and the diagnosis

Ian built a six-member team for Fantina (Hearthome Gym, Fantina's split, cap 33) in the OxiDex on 2026-10-29 and asked for it to be the team to riff off, with an analysis in the style of the last few fights. This page holds stages 1 and 2 of the redesign, the evidence and the diagnosis, for Ian to check. It judges his six as they stand and proposes no new team: candidates and sets are stages 3 and 4. His six is on branch `overseer-fantina` (5a991974dc) for study only; nothing here lands.

## Ian's answers (2026-10-29)

Ian read stages 1 and 2 the same day and answered, relayed by the Overseer:

- Question 2: Competitive stays on Gothitelle.
- Question 5: the off-list moves are made legal through the egg lists, the trainers' palette, which the player never reaches (1c0d086362): Confuse Ray and Body Press on Yamask's, Pain Split on a new Rotom list, Spirit Shackle and Pursuit on Rowlet's, Nasty Plot on Misdreavus's.
- Question 6: the natures are his on purpose. Gothitelle is named Calm; the other five keep the natures the game rolls (Quirky, Relaxed, Mild, Naughty, Bashful).
- Question 7: Runerigus's Amnesia becomes Iron Defense.
- He added Harassment to Fantina's AI flags.
- He is not after a full redesign. He asked for the best replacements for the fight's weakest point, which he and the diagnosis both name as the Runerigus lead, judged by one rule of his: a lead may be countered outright by a Pokemon or a whole type, so long as the counter draws in a member that beats it and has a setup move, since the player then has to switch out while that member sets up. "The lead: three candidates", after stage 2, answers that.

His second save is the file at 1c0d086362. Stage 2 below reads his first, so its points on Amnesia, the natures and the off-list moves are settled by these answers.

## Summary

**Outcome.** Ian's six holds together as a fight: a Ghost gym of burns, confusion and special setup, with Unburden speed on Drifblim and Levitate on the two fastest members, and the trainer AI picked every move on every member in the probe. Four things fail as it stands:

1. Seven moves on four members are in no Oxide list for their species at these levels, so the file is not legal before Cyrus 3's split.
2. No nature is set. Drifblim rolls Relaxed (Speed 58, under the player's Staravia until its berry) and Gothitelle rolls Lonely (Attack up on an all-special set, Defense down).
3. Gothitelle sits nine levels under its evolution and is Bug-weak four times over: Leavanny's Bug Bite knocks it out from full HP (100 to 124 percent), and Leavanny is in 53 of the matchup screen's 60 top sixes.
4. The cheap checks cannot see this team's strength. The screen counts no status move, so it calls the slow physical walls Bastiodon and Probopass clean answers to Drifblim and Mismagius, though both carry setup and Drifblim carries Will-O-Wisp. The fight gets the margin the standing rulings give status and stall teams, or a spot check.

**The fight's shape, in short.** Drifblim, Mismagius and Rotom are the threats: Drifblim doubles its Speed to 116 once its Sitrus Berry goes (over every catch in every box) and carries Calm Mind and Will-O-Wisp; Mismagius is the ace, the fastest member at 83, with Nasty Plot; Rotom is the member the screen finds hardest to answer, since only Ghost and Dark moves hit it super-effectively. Runerigus leads with burns, Confuse Ray and Body Press, which is the team's one hard hit on Bastiodon and Probopass. Gothitelle is the non-Ghost pivot that takes the Dark and Ghost moves the player aims at the other five. The player's answer, by the screen, is Bastiodon, Leavanny and Staravia (with Probopass on box 1 and Hariyama on box 3).

**What Ian checks.**

1. Whether the shape and diagnosis below match how he would plan the fight, and the order he wants the player baited in (which member should meet Leavanny, Bastiodon, Staravia and Hariyama).
2. Gothitelle's ability: the file's slot 2 is Competitive, not the Frisk he named. Which does he want? (Frisk does nothing in the fight; Competitive answers Granbull's Intimidate and the player's Snarl and Icy Wind.)
3. Gothitelle at 32, nine levels under Gothorita's evolution at 41: keep it, use Gothorita, or put another Psychic and Dark Pokemon in the slot?
4. Decidueye at 32, four levels under Dartrix's evolution at 36: fine as it is?
5. The seven moves off Oxide's lists (below): make them legal through the egg lists, which are the trainers' palette only and change nothing the player can learn, or swap them for legal moves?
6. Natures: set all six. Keep the rolled ones that fit (Mild Rotom, Naughty Decidueye) and change Relaxed Drifblim and Lonely Gothitelle? Should Rotom and Mismagius be Timid, which moves them off the knife edges in the speed tiers?
7. Runerigus's Amnesia raises Special Defense only, and Body Press runs off Defense. The AI spends turn one on Amnesia in 66 to 74 of 150 fights whatever the player leads. Keep it, or Iron Defense (on Runerigus's TM list)?
8. Fantina is the first boss allowed a forced trade, and the six carries none. Keep it that way, or add Destiny Bond (legal on Runerigus through Yamask's egg list)?
9. A target. I propose 85 to 90 percent won, level with Roark (86) and Gardenia (90). Since the cheap checks underrate this team's status and setup, I would tune it until they read about 90, expecting the real fight to read harder.
10. Whether to spot-check his six as it stands with a reading on goal 3's three boxes before stage 3, or go on by the cheap checks alone, as Lucas and Dawn 2 did.

**Next steps, once Ian has checked this.** Stage 3, candidate swaps for the faults he wants fixed (Gothitelle's slot, the off-list moves, the natures): an hour or two of a session. Stage 4, the sets and their five-minute check (legality, the probe): about an hour. A spot-check reading, only if he names one: two and a half to four hours, the standing rulings' figure for a boss.

## Stage 1: the evidence

### How the numbers were made

Every number on this page comes from one of these runs, all in the worktree at 5a991974dc:

- The boxes and the matchup screen: `plgoal3 --run fantina-study --box fantina <seed> --screen` for seeds 1 to 3, and `--list` for the play order. The run name has no earlier results, so each box is built without the seed's earlier fights (the QA pass's point 1, accepted on 2026-10-21).
- Each catch's margin against each member, its Speed, and the calculator's damage rows both ways: two scratch scripts in `/home/ian/.claude/jobs/382760ce/tmp/fantina/` (`margins.py` and `probe.py`), which build the same state through plgoal3's own `setup` and `fight_state` and read `plteam.screen` and `plteam.matchups`. Damage is the calculator's lowest to highest roll at no stat stages, as a share of the target's HP, with each trainer member's held item in its rows.
- The AI-picks probe: `probe.py` again (below, "The five-minute check").
- Legality: the Kaizo study's checker (`oxide.check` in `~/oxide-trials/kaizo-teams/out/tools`, with the pre-TM-pass TM lists from 5c62989651, as Ian's rule of 2026-10-07 has it), and the OxiDex's own list (`learnsets.oxide_list`), which agree; the canon sources from `learnsets.lists`.
- The rolled natures and every member's Speed: the scorer's own build of the trainer file.

### Ian's six and its faults

The file has the AI flags Basic, Evaluate Attack, Expert and Setup First Turn (unchanged from the comb's team) and iv_scale 240 on every member, so every IV is 29. No nature is set; the nature in italics is the one the game rolls, as the scorer builds it.

| Member | Level | Item | Ability | Nature | Speed | Moves |
|---|---|---|---|---|---|---|
| Runerigus (lead) | 31 | Leftovers | Wandering Spirit | *Quirky* | 32 | Amnesia, Will-O-Wisp, Confuse Ray, Body Press |
| Drifblim | 32 | Sitrus Berry | Unburden | *Relaxed* | 58 (116 after the berry) | Shadow Ball, Air Cutter, Calm Mind, Will-O-Wisp |
| Rotom (base form) | 32 | Life Orb | Levitate | *Mild* | 72 | Ominous Wind, Shock Wave, Signal Beam, Pain Split |
| Decidueye | 32 | Lum Berry | Overgrow | *Naughty* | 59 | Spirit Shackle, Pursuit, U-turn, Seed Bomb |
| Gothitelle | 32 | Assault Vest | Competitive (slot 2) | *Lonely* | 55 | Dark Pulse, Psyshock, Grass Knot, Thunderbolt |
| Mismagius (ace) | 33 | Shell Bell | Levitate | *Bashful* | 83 | Shadow Ball, Nasty Plot, Draining Kiss, Foul Play |

Faults against the standing rulings:

1. Seven moves are in no Oxide list for their species at these levels (level-up to the member's level, the line's TM, tutor and egg moves, and the pre-TM-pass TMs). Both checkers agree.

   | Member | Move | Where Oxide has it | Where canon has it |
   |---|---|---|---|
   | Runerigus 31 | Amnesia | nowhere | Generation 8 TM |
   | Runerigus 31 | Confuse Ray | nowhere | nowhere |
   | Runerigus 31 | Body Press | Runerigus's level 68 | Generation 8 TM |
   | Rotom 32 | Pain Split | nowhere | Generation 4 tutor |
   | Decidueye 32 | Spirit Shackle | Decidueye's level 40 | on evolving (Generation 9) |
   | Decidueye 32 | Pursuit | nowhere | nowhere |
   | Mismagius 33 | Nasty Plot | nowhere | Generation 4 egg move (Misdreavus) |

   The comb dropped Rotom's Pain Split on 2026-10-07 for this reason. Ian's ruling of 2026-10-13 lets a trainer know a level-up move learned just after the split (Exeggutor's Egg Bomb at 27); Spirit Shackle at 40 is seven levels past the cap and Body Press at 68 is far past it, so neither fits that allowance. Every other move is legal: Will-O-Wisp is Yamask's at 18; Drifblim's four are TM and tutor moves; Rotom's three attacks are its own at 22 to 29; U-turn is Decidueye's level-1 move and Seed Bomb its 32; Gothitelle's are Psyshock at 22 and three TMs; Draining Kiss is Mismagius's 29, Shadow Ball and Foul Play TMs.
2. No member has a set nature (Ian, 2026-10-12: every enemy Pokemon has its own nature). The six rolled ones do not repeat, but two work against their sets: Relaxed lowers Drifblim's Speed to 58 (65 neutral), and Lonely raises Gothitelle's unused Attack and lowers its Defense.
3. Gothitelle is at 32 where Gothita becomes Gothorita and Gothorita becomes Gothitelle at 41: nine levels early, which is past Ian's "not egregiously early" by any reading. Decidueye is four under Dartrix's 36; Lucas and Dawn 2's Gastrodon sat one under its own. Runerigus evolves from Yamask by levelling up with a Reaper Cloth at any level, Drifloon becomes Drifblim at 28, and Mismagius comes from a Dusk Stone, so those three are fine.
4. The items do not repeat (Leftovers, Sitrus Berry, Life Orb, Lum Berry, Assault Vest, Shell Bell), so that rule holds. A Life Orb on a trainer is allowed.

The ability Ian named for Gothitelle, Frisk, is its slot 1; the file asks for slot 2, Competitive, and the scorer reads it so. Its hidden ability is Shadow Tag, which would be a second trap beside Spirit Shackle.

### Against the team it replaces

Drifblim's set is the base ROM's, move for move, and so is Rotom's with Pain Split, which the comb had dropped because Oxide's lists do not hold it. Mismagius stays the ace at 33. The three new lines (Runerigus, Decidueye, Gothitelle) are on no other trainer in the game; the Drifloon line is on three of the gym's own trainers just before (Catherine's Drifblim 31, Mackenzie's and Donny's Drifloons) and the Misdreavus line on three (Allen, Catherine, Molly). The gym's trainers already carry Will-O-Wisp, Pursuit, Confuse Ray and Pain Split, so a player arrives at Fantina warned about burns.

| Team | Members |
|---|---|
| The base ROM's, read by goal 2 on 2026-10-03 | Duskull, Drifblim, Rotom, Sableye, Mismagius |
| The comb's, in the game since 2026-10-07, never read | Froslass (Focus Sash, Spikes), Drifblim, Rotom (Trick for Pain Split), Duskull (Destiny Bond), Sableye, Mismagius (Expert Belt) |
| Ian's six, on this branch | Runerigus, Drifblim, Rotom, Decidueye, Gothitelle, Mismagius |

### Goal 3's three boxes

Built with `plgoal3 --box fantina <seed> --screen` at level 33, the split's cap. Each box has 34 catches, with held-back versions on offer beside them (fourteen on box 2, nine on box 3). Box Speeds are at 33 as goal 3 builds the box (Hardy, IVs 15, no EVs). The screen ranks sixes by matchups alone: for each catch and member, how many more hits the member needs to knock the catch out than the catch needs for the member, from full HP, by damage. Its sixes are a forecast of the player's answers, not the scorer's choice.

How often each catch is in the screen's top 20 sixes:

| Box (starter) | In all 20 | In many | Sometimes |
|---|---|---|---|
| 1 (Turtwig) | Staravia, Probopass | held Luxray 16, Leavanny 13, Bastiodon 7 | Alolan Ninetales 5; Sylveon, Haunter, Golbat 4 |
| 2 (Scorbunny) | Staravia, Leavanny, Bastiodon | Alolan Ninetales 12, Sylveon 9 | 22 others at 1 or 2 |
| 3 (Piplup) | Leavanny, Hariyama, Bastiodon | Orbeetle 8, held Vikavolt 7, Pachirisu 7 | Vullaby, Tentacruel, Salazzle, Rotom 3 |

The held Luxray is the version that reaches Crunch; the held Vikavolt is a Grubbin kept to 30. The player's starter is in 3 of 20 on box 1 and 1 of 20 on box 2, and the Piplup line in 2 of 20 on box 3.

Each member's best answer among the catches the top sixes take, as the screen's margin (a margin of 3 is its cap, a clean win; half a hit is a coin flip on Speed):

| Member | Box 1 | Box 2 | Box 3 |
|---|---|---|---|
| Runerigus | 3: eight catches (Leavanny, Golbat, Haunter, Sylveon and others) | 3: nine catches | 3: eight catches |
| Drifblim | 3: Probopass, Luxray, Bastiodon | 3: Bastiodon | 3: Bastiodon |
| Rotom | 0.5: Probopass, Luxray, Alolan Ninetales, Sylveon | 0.5: Alolan Ninetales, Sylveon | 0.5: Hariyama |
| Decidueye | 1.5: Staravia | 1.5: Staravia | 0.5: Hariyama and four others |
| Gothitelle | 2.5: Luxray, Leavanny | 2.5: Leavanny | 2.5: Leavanny |
| Mismagius | 3: Probopass | 2.5: Bastiodon | 2.5: Bastiodon |

Damage that decides the matchups, lowest to highest roll, as a share of the target's HP:

| Attacker and move | Target | Damage |
|---|---|---|
| Leavanny's Bug Bite (boxes 1 to 3) | Gothitelle | 100 to 124% |
| Orbeetle's Bug Buzz (box 3) | Gothitelle | 100 to 120% |
| Held Luxray's Crunch (box 1) | Drifblim, Mismagius, Decidueye, Rotom | 120 to 144, 102 to 122, 90 to 108, 78 to 92% |
| Hariyama's Knock Off (box 3) | Drifblim, Mismagius, Decidueye, Rotom | 70 to 84, 60 to 72, 54 to 64, 44 to 54% |
| Alolan Ninetales's Icicle Spear (boxes 1, 2) | Drifblim, Decidueye | 96 to 114, 72 to 90% |
| Staravia's Dual Wingbeat (boxes 1, 2) | Decidueye | 64 to 76% |
| Leavanny's Razor Leaf | Runerigus | 32 to 42% |
| Bastiodon's Metal Claw, before any burn | Drifblim, Mismagius | 31 to 37, 27 to 33% |
| Rotom's Shock Wave | Staravia | 138 to 164% |
| Gothitelle's Thunderbolt; its Psyshock | Staravia; Hariyama | 98 to 116; 98 to 116% |
| Drifblim's Air Cutter | Leavanny; Hariyama | 100 to 124; 66 to 78% |
| Rotom's Signal Beam | Leavanny | 68 to 82% |
| Runerigus's Body Press | Probopass, Bastiodon, Luxray, Hariyama | 57 to 69, 51 to 63, 66 to 78, 41 to 49% |
| Mismagius's Shadow Ball, unboosted | Bastiodon, Probopass; Hariyama | 14 to 17, 13 to 16; 58 to 69% |
| Any Ghost move | Staravia | 0: immune |

### The old reading, and the neighbours

Fantina's only reading is goal 2's of 2026-10-03, of the base ROM's five (`fight-difficulty-ranking.md`): 91 percent won, 3.04 faints a fight, 1 percent clean, difficulty 6.77, on goal 2's box and the simulator of that day. The ranking also has a stale row for the Kaizo team at 40 percent won. The comb's team in the game today has never been read, and neither has Ian's six.

| Fight | Reading | Won |
|---|---|---|
| Roark, in the game | goal 3, 2026-10-13 (boxes 81, 77, 99) | 86% |
| Somnu 1 | goal 3, 2026-10-22 (88, 96, 97) | 94% |
| Mars 1 | goal 3's second reading, 2026-10-22 (57, 17, 100), before Ian's dials, not read since | 58% |
| Gardenia, in the game | goal 3, the locked team (99, 87, 83) | 90% |
| Moira 1 | goal 3, before Ian's changes, not read since | 100% |
| Jupiter 1 | goal 3, 2026-10-22 (99, 75, 93) | 89% |
| Lucas and Dawn 2 | Ian's target, not read | 90 to 94% |
| Fantina, the base ROM's five | goal 2, 2026-10-03 | 91% |

The targets from the standing rulings: no boss above 95 percent won, spiking with the boss's importance, the hardest near 80. Fantina is the third gym leader and closes her split, so she should read at least as hard as the officers and Lucas and Dawn 2 before her. The proposal in the summary, 85 to 90, puts her level with Roark and Gardenia.

### Speed tiers

Each member's Speed against the boxes' fastest catches and the screen's core answers. The members' Speeds with a nature that lowers, leaves or raises Speed are shown for the ones a set nature could move.

| Speed | Fantina's members | The player's catches |
|---|---|---|
| 116 | Drifblim after its Sitrus Berry (130 neutral) | |
| 86 to 91 | Mismagius Timid 91 | Salazzle 87 (box 3), Liepard 86 (box 2) |
| 83 | Mismagius as rolled | Haunter 82 (box 1) |
| 75 to 79 | Rotom Timid 79 | Tentacruel, Alolan Ninetales 75 |
| 70 to 72 | Rotom as rolled 72, Drifblim with a Speed nature 71 | Luxray, Sharpedo 72 (box 1); Pachirisu, Leafeon 72 (box 3); Raboot 71; Leavanny, Rotom, Tsareena, Lumineon 70 |
| 60 to 69 | Drifblim neutral 65 | Golbat, Orbeetle, Ponyta 69; Dubwool 68; Pawmo, Cherrim 66; Fletchinder 65; Staravia 62; Corvisquire, Mothim 60 |
| 55 to 59 | Decidueye 59, Drifblim as rolled 58, Gothitelle 55 | Kingler 59; Bibarel, Seaking, Onix, Breloom 56 |
| 42 to 52 | | Nidorino 52; Whiscash, Vullaby, Sylveon 49; Hariyama, Carbink 42 |
| 29 to 36 | Runerigus 32 | Probopass 36, Bastiodon 29 |

Mismagius outspeeds every catch but Liepard and Salazzle, and Drifblim outspeeds everything once its berry goes. The knife edges, the kind that swung Gardenia:

- Rotom at 72 ties box 1's held Luxray, whose Crunch takes 78 to 92 percent, and Sharpedo, and box 3's Pachirisu and Leafeon. A tie is a coin flip each turn. Timid (79) puts it over all of them, and over Tentacruel and Alolan Ninetales (75) too.
- Mismagius at 83 is one point over box 1's Haunter (82), which hits it super-effectively. Timid (91) puts it over Liepard and Salazzle too.
- Drifblim, rolled Relaxed, sits at 58 until its berry: under Staravia (62) and Corvisquire (60), and one under Kingler (59). Neutral, it is at 65, over all three.
- Decidueye at 59 ties Kingler.
- Leavanny (70) moves before Decidueye, Drifblim before its berry, and Gothitelle, but after Rotom and Mismagius.

### The five-minute check: what the AI picks

The probe follows Lucas and Dawn 2's. Somnu 1's scratch probe was its model: rough fights of the trainer's six against a greedy player, who takes its hardest-hitting move by the lowest roll 85 percent of the time and a random legal action otherwise, with the player holding no items. It ran on each of goal 3's boxes, with each catch's four moves as the screen picked them, against two sixes: the screen's best six, and a six of the catches its top 20 take most. That makes six runs of 150 fights. The win and faint numbers mean nothing; what counts is which moves the AI picks and which items fire.

| Member | Moves, by how often the AI picked them over the six runs | Note |
|---|---|---|
| Runerigus | Body Press 383 to 653, Will-O-Wisp 138 to 312, Confuse Ray 132 to 202, Amnesia 96 to 112 | Its first move is a status move in 147 to 150 of 150 fights in every run, Amnesia in 66 to 74 of them, whatever the player leads |
| Drifblim | Shadow Ball 199 to 475, Air Cutter 113 to 240, Will-O-Wisp 62 to 178, Calm Mind 67 to 118 | Its Sitrus Berry went, and Unburden with it, in 93 to 147 of 150 fights |
| Rotom | Shock Wave 33 to 251, Ominous Wind 23 to 159, Signal Beam 54 to 138, Pain Split 10 to 39 | Pain Split is its least picked move in every run |
| Decidueye | Seed Bomb 53 to 202, Spirit Shackle 41 to 177, Pursuit 28 to 78, U-turn 8 to 52 | Its Lum Berry went in 9 to 34 fights |
| Gothitelle | Grass Knot 41 to 265, Dark Pulse 26 to 107, Psyshock 23 to 114, Thunderbolt 14 to 63 | Grass Knot leads on box 1, where it is Gothitelle's best hit on Probopass and Bastiodon; on box 3 Gothitelle is picked least of the six |
| Mismagius | Shadow Ball 160 to 357, Nasty Plot 44 to 101, Draining Kiss 20 to 82, Foul Play 20 to 56 | |

Every move on every member was picked in every run. On box 3, Hariyama's Knock Off took Runerigus's Leftovers in 91 to 92 of 150 fights, Rotom's Life Orb in 6 to 19 and Mismagius's Shell Bell in 5 to 17. As a rough sign only, the members in when the greedy player's Pokemon fell were Drifblim (1,172 over the six runs) and Mismagius (1,105) most, then Runerigus (831) and Rotom (791), then Gothitelle (554) and Decidueye (431).

## Stage 2: the diagnosis

### The fight's shape

Written as `boss-shapes.md` frames the others. How sure: a forecast from the screen, the damage rows and the probe, not from a reading, since no team of Fantina's has been read since 2026-10-03.

**Identity.** Fantina's Ghost gym, five Ghosts and one Psychic and Dark Pokemon, fighting with burns, confusion and special setup. Two members float (Rotom and Mismagius, by Levitate) and one flies (Drifblim), so half the team ignores Ground moves, Spikes and Sticky Web.

**The boss's core:**

- Drifblim: Unburden after its Sitrus Berry, which doubles its Speed to 116, over every catch in every box; Calm Mind at 3 PP; Will-O-Wisp for the physical answers; Air Cutter on Leavanny four times over.
- Mismagius, the ace at the cap: the fastest member at 83, Nasty Plot at 1 PP, Shadow Ball, and Foul Play, which runs off the player's own Attack.
- Rotom: Levitate on Electric and Ghost leaves it weak only to Ghost and Dark, and its Life Orb Shock Wave knocks out Staravia, which is in every top six of boxes 1 and 2. No catch the screen takes answers it by more than half a hit.
- Runerigus's Body Press, the team's one hard hit on Bastiodon and Probopass (four times super-effective), and its Will-O-Wisp and Confuse Ray from the lead.

**The player's core counterpieces** (from the screen's sixes, to be confirmed by a reading):

- Bastiodon: in all 20 sixes on boxes 2 and 3 and 7 on box 1, the screen's answer to Drifblim and Mismagius, since nothing but Body Press hurts it.
- Leavanny: in all 20 on boxes 2 and 3 and 13 on box 1, for Bug Bite on Gothitelle and Razor Leaf on Runerigus. Its screen set carries Sticky Web, which three of the six ignore.
- Staravia: in all 20 on boxes 1 and 2. Normal and Flying, it is immune to every Ghost move and hits Decidueye with Dual Wingbeat.
- Probopass (box 1, all 20), the held Luxray with Crunch (box 1, 16), Hariyama with Knock Off (box 3, all 20).
- Not the Dark types: Vullaby, Liepard, Sharpedo and Nuzleaf are in 0 to 3 sixes each, and the player's own Ghosts (Haunter, box 2's and 3's Rotom) in 1 to 4.

**Material for this fight:** the six members' sets, abilities, items and natures; Leavanny's, Bastiodon's and Staravia's availability before Hearthome and their moves; Probopass, the Shinx line's Crunch, and Hariyama's Knock Off; the Speed of any member or catch near the tiers named above; and the simulator's handling of Unburden, Will-O-Wisp, Spirit Shackle and Levitate against hazards.

### Where the screen's bias bites

The screen's answers count only a clean one-on-one from full HP by damage, which overstated Mars 1's Purugly. Here the bias is larger, because four members carry moves the screen does not see at all: Will-O-Wisp twice, Confuse Ray, Amnesia, Calm Mind, Nasty Plot and Pain Split.

1. **Bastiodon and Probopass are overstated.** The screen gives each a clean win over Drifblim and Mismagius, because those two hit it for 13 to 17 percent. But both walls are physical and slow, and their hits are small: Bastiodon's Metal Claw does 31 to 37 percent to Drifblim before a burn and half that after one. Drifblim burns it and Calm Minds; Mismagius's Nasty Plot doubles Shadow Ball to about 28 to 34 percent a hit. Their Taunt is the real answer, and it comes after the setup move, since both are slower than Drifblim and Mismagius.
2. **Every physical answer loses half its damage to a burn.** Staravia, Leavanny, Bastiodon, Probopass, Hariyama and the held Luxray are all physical. Between them the two Will-O-Wisps were picked 200 to 490 times a run. The screen's sixes take almost no Fire types, which are immune (Fletchinder, Ponyta, Raboot and Salazzle are in 1 to 3 sixes each), so a planning player has more reason to bring one than the screen shows.
3. **Speed after the berry.** The screen reads Drifblim at 58, its Speed before Unburden. After the berry it outspeeds every catch, which turns a few of the screen's half-hit margins against it.
4. **Status and stall in a long fight.** Leftovers, Pain Split, Shell Bell, Draining Kiss and Amnesia all pay over many turns, which the cheap checks underrate (the standing rulings). Jupiter 1's sealed prediction missed its box 2 by ten points on the hard side, and it had under-weighted the status and stall pieces. So the team needs a margin, or a spot check where a box looks thin.

The bias also runs the other way for Runerigus. The screen counts eight or nine clean answers to it on every box because its only attack is Body Press, but its job is the burns and the confusion, and it has the bulk (base Defense 145) to land them.

### What fails under baiting

Ian plans a boss by baiting matchups in the order he wants. Against his six:

1. **The lead is known, and slow.** Runerigus leads at Speed 32, and its first move is a status move in nearly every fight, Amnesia in about half. A player who leads a Ghost (box 1's Haunter, box 2's or 3's Rotom) is immune to Body Press and hits it super-effectively. A Taunt lead stops its status: Probopass, Corvisquire and Bibarel move first, Bastiodon (29) after it. Body Press still hits the two Steel walls four times over. A Fire lead is immune to Will-O-Wisp. Leavanny leads to set Sticky Web, which slows only Runerigus, Decidueye and Gothitelle.
2. **The replacement order is predictable.** After a faint, the trainer AI sends the member whose own types hit the player's active Pokemon hardest, if it has a super-effective move on it (the rule Lucas and Dawn 2's diagnosis traced). With Leavanny out, Drifblim's Flying type comes in, and its Air Cutter knocks Leavanny out. With Bastiodon or Probopass out, Runerigus's Ground type comes in with Body Press. With Staravia out, Rotom comes in with Shock Wave. With Hariyama out, Drifblim's Flying or Gothitelle's Psychic does. So the player knows which member each switch draws and can keep that member's answer behind it.
3. **Gothitelle is a free knockout for the Bug types the player already brings.** Bug Bite, Bug Buzz and X-Scissor each take 100 to 124 percent from full HP, and Assault Vest does nothing against Bug Bite, a physical move, while the rolled Lonely nature lowers its Defense. Leavanny comes for Gothitelle and Runerigus and is in 53 of the 60 top sixes.
4. **Drifblim is beaten before its berry.** At 58 it moves after Staravia, Corvisquire and Kingler, and box 1's held Luxray knocks it out with Crunch from full HP (120 to 144 percent), so the Sitrus Berry never goes. Box 3's Hariyama Knock Off takes 70 to 84 percent and removes the berry without letting it heal.
5. **Knock Off strips the team's items on box 3.** In the probe, Hariyama took the Leftovers in about 60 percent of fights. Every member's set leans on its item.
6. **Decidueye's set partly undoes itself.** Spirit Shackle traps a non-Ghost while Decidueye stays in, and U-turn ends the trap. Pursuit is redundant on a trapped target; it pays against the player's Ghosts (Haunter, Rotom), which escape the trap and take Dark moves super-effectively. The AI picked U-turn least of its four in five of the six runs.

### Gothitelle, the one non-Ghost

The five Ghosts are immune to Normal and Fighting moves, so the player's Normal and Fighting attacks (Staravia's Take Down, Hariyama's Arm Thrust, Bastiodon's Take Down, Dubwool, Bibarel, Granbull, Pawmo and Machoke) have one target, Gothitelle: Take Down takes 34 to 42 percent and Arm Thrust 36 to 48. Gothitelle is the team's answer to the moves the player aims at Ghosts. As a Psychic and Dark type, Dark moves and Ghost moves both land on it neutrally, and Psychic moves cannot touch it. Its Dark Pulse hits the player's Ghosts and Psychic types (Orbeetle 54 to 66 percent), Psyshock hits Hariyama for 98 to 116 percent, Thunderbolt the Flying types, and Grass Knot the heavy Steel walls.

The cost is two weaknesses: Fairy, and Bug four times over. The player's answer to Gothitelle is the Bug type that also beats Runerigus. In theme it reads as Fantina's gothic side, but its own line is nine levels short of this stage. Against the Dark types, which the Ghosts fear most, the team already has coverage on four other members: Body Press (Fighting), Signal Beam and U-turn (Bug), and Draining Kiss (Fairy).

### Abilities and items

- **Wandering Spirit** is Runerigus's only ability. It swaps abilities with a Pokemon that makes contact, which rarely matters here. It gives Runerigus nothing it needs and takes little from the player.
- **Unburden** is the team's best ability: the probe saw the berry go in most fights.
- **Levitate** on Rotom and Mismagius blanks Ground moves and the hazards. Box 3's Pachirisu has Mud Shot, and the screen's Bastiodon and Probopass have Bulldoze, all of which do nothing to them.
- **Overgrow** on Decidueye boosts one Grass move only in the red, so it is close to dead.
- **Competitive** (what the file has) raises Gothitelle's Special Attack two stages when the player lowers a stat: Granbull's Intimidate (on boxes 1 to 3), Orbeetle's and Vullaby's Snarl, and Icy Wind from Haunter, Whiscash and Tentacruel. **Frisk** (what Ian named) only shows the player's items and does nothing in the fight.
- **Life Orb** on Rotom pays for its Pain Split, which the AI rarely picks (10 to 39 times a run against 33 to 251 for Shock Wave), so the recoil is mostly unpaid back.
- **Shell Bell** heals an eighth of the damage Mismagius deals, a few HP a hit before Nasty Plot. It is thin beside a Sitrus Berry or Leftovers, but it is not a repeat.
- **Assault Vest** fits a Gothitelle with four attacks, and it guards against the special Bug Buzz but not against the physical Bug Bite and X-Scissor that threaten it most.
- **Lum Berry** on Decidueye answers a burn or paralysis from the player (Will-O-Wisp and Thunder Wave are in Fletchinder's, Plusle's and Probopass's move pools) and went in 9 to 34 fights.

### Natures

Six rolled natures, none repeated, none set. What each does today:

| Member | Rolled | Effect on its set |
|---|---|---|
| Runerigus | Quirky | Neutral. Body Press runs off Defense, so a Defense-raising nature (Bold or Impish) would raise both its hits and its bulk |
| Drifblim | Relaxed | Speed 58 instead of 65, under Staravia and Corvisquire until its berry |
| Rotom | Mild | Special Attack up and Defense down, which suits it |
| Decidueye | Naughty | Attack up and Special Defense down, which suits a physical set |
| Gothitelle | Lonely | Attack up, unused by four special moves, and Defense down, where the player's Bug and Normal moves land |
| Mismagius | Bashful | Neutral; Timid would move it over Liepard and Salazzle |

### Status, setup, trapping and trades

The team carries two Will-O-Wisps, Confuse Ray, three stat-raising moves (Amnesia and Nasty Plot at 1 PP, Calm Mind at 3, as the setup-PP ruling has them), Pain Split, Draining Kiss and two healing items. The cheap checks undercount every piece of it, so the target above should be read with a margin.

Amnesia is a poor fit. It raises Special Defense, which Runerigus already has at base 105, and does nothing for Body Press, which runs off Defense. With Setup First Turn, the AI spends Runerigus's first turn on it in about half of all fights, whatever the player leads, so against the physical leads the screen expects it wastes the lead's best turn. Iron Defense, on Runerigus's TM list, would power Body Press instead; Calm Mind and Curse are also in its palette.

Spirit Shackle is the team's one trapping move, within the rule that trapping is rare. The six carries no forced trade. Fantina is the first boss allowed one (Explosion, Self-Destruct or Destiny Bond), and Destiny Bond is legal on Runerigus through Yamask's egg list; the comb's team had it on Duskull.

### Each member's job

**Runerigus, the lead.** It lands burns and confusion from a bulky body and threatens the Steel walls with Body Press. It works against the physical leads the boxes bring, but it is slow, its Amnesia fits nothing on its set, and three of its four moves are off Oxide's lists.

**Drifblim.** The team's speed control and its answer to Leavanny and Hariyama. It is held back by its rolled Relaxed nature, which leaves it under Staravia until its berry, and by Crunch and Knock Off from the player's box 1 and box 3.

**Rotom.** The member the player has least for. Its Shock Wave punishes the Staravia every top six on boxes 1 and 2 brings. It ties four catches at 72, and Pain Split is off-list and rarely picked.

**Decidueye.** The physical Grass and Ghost hit, with Seed Bomb on the Water and Ground types and Spirit Shackle to hold a target. It had the fewest knockouts in the probe's rough count, it is four levels under its evolution, and two of its moves are off-list.

**Gothitelle.** The pivot for Dark and Ghost moves, and the one target for the player's Normal and Fighting moves. Its Bug weakness makes it Leavanny's free knockout, and it is nine levels under its evolution with a nature that works against it.

**Mismagius, the ace.** The fastest member with the strongest setup. Bastiodon and Probopass are the screen's only clean answers to it, and only until it has set up or they are burned. Its Nasty Plot is off-list, and a Timid nature would clear the two catches still faster than it.

## The lead: three candidates

Ian asked for the best replacements for the Runerigus lead, judged by his rule that a lead may be countered outright if the counter draws in a member that beats it and has a setup move. Four Ghost leads were checked against his Runerigus with Iron Defense, on the file at 1c0d086362 with Harassment on. One of them, Sableye, failed. The finding first: by Ian's rule, his Runerigus is the best lead of the five, and no replacement beats it at that job. The three candidates below are what to reach for if he wants a different fight.

### How they were checked

Each candidate replaced Runerigus in memory only, with the other five members as in the file; `res/` was not written. Two scratch scripts in `/home/ian/.claude/jobs/382760ce/tmp/fantina/` ran on goal 3's boxes 1 to 3. `lead.py` reruns the matchup screen, the Speeds, the damage rows both ways, and the AI-picks probe (two runs of 150 rough fights a box, as in stage 2). `repl.py` finds what each of the lead's counters draws in. It sets the lead fainted with the counter on the field and calls the simulator's own copy of the engine's replacement rule, `fightai.replacement` (BattleAI_PostKOSwitchIn), rather than reasoning from types. It then reads the screen's margin of the counter against the member drawn. A counter here is a catch the screen gives a win over the lead one-on-one, plus every Ghost, Fire and Taunt catch in the box. Every candidate set passes the Kaizo study's legality checker with the pre-TM-pass lists, and no item or nature repeats.

| Lead | Level | Item | Ability | Nature | Speed | Moves |
|---|---|---|---|---|---|---|
| Runerigus (Ian's) | 31 | Leftovers | Wandering Spirit | *Quirky* | 32 | Iron Defense, Will-O-Wisp, Confuse Ray, Body Press |
| Haunter | 31 | Focus Sash | Levitate | Timid | 90 | Shadow Ball, Focus Blast, Will-O-Wisp, Destiny Bond |
| Dusknoir | 33 | Leftovers | Levitate | Adamant | 44 | Earthquake, Will-O-Wisp, Shadow Sneak, Ice Punch |
| Ceruledge | 31 | Leftovers | Flash Fire | Jolly | 72 | Brick Break, Shadow Claw, Flame Charge, Will-O-Wisp |
| Sableye (set aside) | 31 | Leftovers | Prankster | Impish | 44 | Will-O-Wisp, Drain Punch, Knock Off, Taunt |

Haunter is the line's own stage at 31 (Gastly evolves at 25, Haunter at 40). Its Destiny Bond is the fight's one forced trade, which Fantina is the first boss allowed, and a Focus Sash may go on the lead that carries it (Ian, 2026-10-06). Dusknoir at 33 sits four levels under Dusclops's evolution at 37, as Decidueye does under Dartrix's, and it needs a Reaper Cloth past that. Ceruledge comes from Charcadet with a Dusk Stone, at any level.

### What the cheap checks show

| Lead | The player's best six by the screen, boxes 1, 2, 3 (lower is harder) | Catches that beat the lead one-on-one, per box | Body Press or its stand-in on Bastiodon; on Probopass | Its first move, by the AI, in each run of 150 | The player's Pokemon knocked out while it was in (rough sign) |
|---|---|---|---|---|---|
| Runerigus | 16.8, 14.55, 12.8 | 18, 20, 20 | Body Press 51 to 63; 57 to 69% | Will-O-Wisp 43 to 65, Confuse Ray 44 to 54, Iron Defense 36 to 54, Body Press 0 to 1 | 184 to 333 |
| Haunter | 14.85, 12.3, 9.55 | 5, 5, 5 | Focus Blast 75 to 90; 69 to 84% | Will-O-Wisp 115 to 138, Shadow Ball 8 to 21, Focus Blast 3 to 21 | 134 to 174 |
| Dusknoir | 10.4, 8.15, 6.4 | none | Earthquake 60 to 72; 66 to 81% | Will-O-Wisp 90 to 139, Ice Punch 2 to 41, Earthquake 3 to 37 | 221 to 402 |
| Ceruledge | 14.55, 12.45, 10.55 | 9, 8, 10 | Brick Break 42 to 51; 51 to 60% | Will-O-Wisp 97 to 123, Flame Charge 13 to 37, Brick Break and Shadow Claw 4 to 13 each | 120 to 165 |
| Sableye | 16.65, 14.55, 12.5 | 8, 8, 9 | Drain Punch 36 to 45; 42 to 51% | Will-O-Wisp 88 to 134, Taunt 10 to 48, Drain Punch 3 to 42 | 41 to 98 |

With Harassment on, Runerigus's first move is still a status move in 149 or 150 fights of every 150, but it now spreads across its three status moves. Iron Defense comes up against every kind of lead, most often Alolan Ninetales (13 and 21 of the 25 fights it leads in on box 2), and each use powers Body Press, where Amnesia had powered nothing. Every move of every candidate was picked in every run, except Sableye's Knock Off, which the AI never chose, and that is one reason it is set aside. The other is that it made the fewest knockouts of the five.

### What the counters draw in

The member the AI sends after the lead faints depends on the counter and on the other five, which are the same for every lead. So the same counter nearly always draws the same member, and a lead is judged by which catches counter it. Over the three boxes, `fightai.replacement` gives:

| The lead's counter | Member drawn in | Does it beat the counter (screen margin) | Setup |
|---|---|---|---|
| The Grass and Bug catches: Leavanny (every box), Breloom, Roselia, Leafeon, Cherrim, Tsareena, Vikavolt, Mothim, Orbeetle, Masquerain, Dustox, Heracross | Drifblim | Yes, by 0.5 to 6.5 (Leavanny 6.5) | Calm Mind |
| Hariyama, Granbull | Drifblim | Yes, by 0.5 | Calm Mind |
| Rotom (boxes 2, 3) | Mismagius | Yes, by 0.5 | Nasty Plot |
| Torterra, Bronzong; Alolan Ninetales | Drifblim | No: the catch wins by 0.5; by 2.5 | Calm Mind |
| The Water catches (Seaking, Kingler, Tentacruel, Lumineon, Brionne, Prinplup), Golbat, Vullaby, Togetic, Liepard; the Taunt users Bibarel and Corvisquire; Fletchinder | Rotom | Yes, by 0.5 to 6.5 | none |
| Whiscash, Quagsire, Donphan, Sylveon, Carbink, Onix, Graveler; Bastiodon's Taunt | Decidueye | Yes, by 0.5 to 7.5 | none |
| Haunter (box 1); Salazzle (box 3) | Gothitelle | Yes, by 2.5; by 1.5 | none |
| Raboot and Ponyta (box 2), Probopass's Taunt, Luxray (box 1, every version) | Decidueye | No: the catch wins by 0.5 | none |

Each lead's counters, read against that table:

- **Runerigus**: its 18 to 20 counters a box are mostly the Grass, Bug and Fairy types, and those are what draw Drifblim's Calm Mind. Leavanny, the catch the screen takes most against this team, beats Runerigus and draws Drifblim, which beats it by the widest margin on the table. Over the three boxes (counting the held Luxrays and Vikavolt as entries of their own), 22 of its counters draw a setup member that beats them, 31 a member that beats them without setup, and 8 a member that loses.
- **Haunter**: its five counters a box are Luxray, Alolan Ninetales, Torterra, Tentacruel, Vullaby, Masquerain, Hariyama, Vikavolt and Bronzong. Six of its fifteen counters over the three boxes draw a member that loses (Luxray draws Decidueye; Ninetales, Torterra and Bronzong draw Drifblim), so its counters fit Ian's rule worst. Its Destiny Bond often takes the counter with it. The AI also switches it out 15 to 88 times a run.
- **Dusknoir**: no catch beats it one-on-one, so the rule never comes into play. It lowers the player's best screen score by 6 points or more on every box, the largest change of any candidate, and it made the most knockouts.
- **Ceruledge**: its 8 to 10 counters a box are the Water, Ground and Rock catches, and they draw Rotom or Decidueye, which beat them with no setup. Only Hariyama draws a setup member.

### The three candidates

1. **Haunter** (Focus Sash, Timid; Shadow Ball, Focus Blast, Will-O-Wisp, Destiny Bond). It answers "slow and known": at 90 it outspeeds every catch in every box, so it burns or hits before any Taunt. Focus Blast takes Bastiodon 75 to 90 percent and Probopass 69 to 84, more than Body Press does. It carries the fight's one trade behind its Sash. It costs the rule's fit, since its counters draw losers, and it repeats the Haunters on two of the gym's trainers.
2. **Dusknoir** (Leftovers, Adamant; Earthquake, Will-O-Wisp, Shadow Sneak, Ice Punch). It answers every lead the diagnosis named: Earthquake for the Steel walls and the Fire leads (Raboot 92 to 110 percent, Salazzle knocked out), Ice Punch for Staravia (102 to 122) and Leavanny, and Shadow Sneak for the Ghosts. It moves the fight the most, likely too far for the 85 to 90 target, and it sits two stages early.
3. **Ceruledge** (Leftovers, Jolly; Brick Break, Shadow Claw, Flame Charge, Will-O-Wisp). It is the middle choice: 72 Speed, immune to the Fire leads' moves through Flash Fire and to burns, and Flame Charge knocks out Leavanny (160 to 192 percent). Brick Break is weaker on the Steel walls than Body Press (42 to 60 percent), and its counters draw no setup.

### Recommendation

Keep Runerigus with Iron Defense. By Ian's rule it is the best lead of the five. Its counters are the Grass and Bug types that draw Drifblim's Calm Mind, Leavanny first among them. Iron Defense now gives it a setup move that feeds Body Press, and Harassment spreads its first turn across its three status moves. Its remaining holes are the counters that draw a member that loses: the Fire leads Raboot and Ponyta, Probopass's Taunt, and the box 1 Luxray, all of which draw Decidueye, and Alolan Ninetales, which draws Drifblim. Those are set changes on the other members, not reasons to change the lead. If Ian wants a different fight rather than this one tightened, Haunter is the pick, and Dusknoir only if he wants Fantina to read clearly harder.

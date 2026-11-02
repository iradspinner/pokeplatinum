# Commander Saturn 1: a check of Ian's first draft

Ian drafted Saturn 1's new six in his OxiDex on 2026-11-02. Saturn is a Galactic commander, so a boss, fought in Valor Cavern in Candice's split (cap 56) after Officer Hesperid 1, with his ace at 53 as Ian set it. This is the check his Hesperid 1 and Mars 2 drafts had ([hesperid-check.md](hesperid-check.md), [mars2-check.md](mars2-check.md)): anything that invalidates the fight, each member's job, the weakest crux with the top picks for it, and the cheap checks. The draft is on branch `overseer-saturn1-check`, saved as it stands. The only other change to the game's data is the egg-list commit for its three off-list moves. No team change was made, no scorer reading was run, and the simulator was not touched.

## Ian's answers (2026-11-02)

1. Azelf holds a Babiri Berry in place of its Focus Sash, and Glimmora keeps the lead's Sash.
2. Naganadel is Rash in place of Hasty, so Beast Boost raises its Sp. Atk.
3. Azelf takes Dazzling Gleam in place of its Stealth Rock. Ian chose it over Drain Punch.
4. The AI flags stay Basic, Evaluate Attack and Expert.
5. Saturn 1's theme line in [boss-shapes.md](boss-shapes.md) is now poison and hazards; Saturn 2 at the HQ keeps the permanent Trick Room.
6. No scorer reading: Saturn 1 is judged in Ian's playtest.

The three edits went through `trainers.save`. No item and no nature repeats: the items are Focus Sash, Leftovers, Life Orb, Yache Berry, Babiri Berry and Poison Barb, and the natures Hasty, Bold, Rash, Mild, Timid and Modest. Dazzling Gleam is Azelf's TM05, so both checkers pass it at 51 and no egg list was needed; the OxiDex's lists give all 24 moves and the Kaizo checker finds 0 problems. The lint finds nothing, the packer packs the file, test_b1 passes 50 of 50, test_learnrewrite 6 of 6, test_learncheck 18 of 18 and test_trainers 44 of 44, and `make rom` builds.

The AI-picks probe was run again on the saved file, on the same three boxes, per six over 150 fights:

| | Ian's draft | After the answers |
|---|---|---|
| The player's wins, mean of the three boxes | 62 | 29 (34, 26; 25; 29, 37) |
| Naganadel's Beast Boost raising Sp. Atk | 0 | 161 to 335 |
| Naganadel's Beast Boost raising Speed | 105 to 154 | 0 |
| Knocked out while Naganadel was in | 130 to 166 | 190 to 362 |
| The player's Pokemon poisoned by Toxic Spikes coming in | 220 to 463 | 116 to 367 |
| Naganadel's Hex and Venoshock into a poisoned target | 49 to 148 | 17 to 146 |
| Glimmora's Toxic Spikes and Stealth Rock | 117 to 134, 104 to 126 | 114 to 148, 106 to 125 |
| Azelf's Dazzling Gleam | | 30 to 95 |
| Azelf's Babiri Berry eaten | | 47 to 106 |
| Knocked out while Azelf was in | 130 to 175 | 155 to 243 |

The poison plan is intact: Glimmora lays both hazards as before, and the payoff still lands. The counts of poisoned entries fall a little because fights end sooner. Rash moves Naganadel's Speed from 158 to 144, under Crobat (150) and Talonflame (146), and its Sp. Atk from 150 to 165. The fight now reads about as the old team did (34), harder than Candice (48), Hesperid 1 and Mars 2 (71 each), and easier than Cyrus 1 (4), so Saturn 1 is the split's hardest fight again.

The sections after this one are the check's, from before these answers.

## Summary

**What could not be checked, first.** Nothing was seen in game. No scorer reading exists for Saturn 1, old or new, so the counterpiece check (the sixes that beat the old team, played against the new one) cannot run, and the probe cannot say on its own whether the fight sits under the 95 percent ceiling for a boss (decision 6).

**Outcome.** Nothing in the engine, the simulator or the AI breaks the fight. Every piece of the draft's idea runs in both, and the AI scores each one: Toxic Spikes and Toxic Debris, Venoshock and Hex doubling into a poisoned target, Corrosion's Toxic on Steel types, the Focus Sashes, the Life Orb with Beast Boost, Apple Acid's drop, Dragon Tail's drag into the hazards, Tailwind, Confuse Ray with Aqua Ring, and Nasty Plot. The levels are under the cap, with the ace at 53. Three moves were on no list; they are now on Mantyke's and Tropius's egg lists. The draft breaks the no-repeats rule twice, with two Focus Sashes and two Hasty natures (decisions 1 and 2).

The idea works as Ian built it. Glimmora lays Toxic Spikes and Stealth Rock in nearly every fight, the player's Pokemon are poisoned coming in 220 to 463 times a six over 150 fights, and Naganadel's Hex and Venoshock land doubled on a poisoned target 49 to 148 times a six. On the probe the draft reads easier than the old team: the player wins 62 rough fights of 150 on average, against the old team's 34. It now sits with Hesperid 1 and Mars 2 (71 each) and a little easier than Candice (48). The old team was the split's hardest fight.

**The weakest crux is Bastiodon.** It is in 15 to 20 of the screen's top 20 sixes on every box and beats all six of Saturn's members one on one. Whichever member falls to it, the AI's replacement rule sends in Mantine, which loses to it narrowly, or Azelf once Mantine is the one gone. Two smaller things leak power. Hasty makes Naganadel's Speed its highest stat, so Beast Boost raises Speed after each knockout, 105 to 154 times a six, and never its Sp. Atk. Azelf's Stealth Rock does nothing once Glimmora has laid the rocks, so it is used only 20 to 42 times a six, when Glimmora has not.

**What Ian decides.**

1. The two Focus Sashes: Azelf takes a Babiri Berry and Glimmora keeps the lead's Sash (my pick; the fight reads harder, 46 against 62); Azelf keeps the Sash and Glimmora takes a Shuca Berry (reads as the draft, 62); or Azelf takes Wise Glasses (not probed)?
2. The two Hasty natures: Naganadel takes Rash, so Beast Boost raises its Sp. Atk, at Speed 144 instead of 158 (my pick; with decision 1's pick the fight reads 30, about as the old team); Glimmora takes Naive, keeping its Defense for Toxic Debris, at the same Speed; or Naganadel takes Naive, at the same Speed, with Beast Boost still raising Speed?
3. Azelf's second Stealth Rock: Drain Punch (TM60) in its place, a Fighting hit for Bastiodon and the Rock types that also heals (my pick; with decisions 1 and 2 the fight reads 18, the split's hardest again but still easier than Cyrus 1 at 4); Dazzling Gleam (TM05), its Fairy attack (reads 58 alone); or keep it as a backup setter?
4. The AI flags: keep Basic, Evaluate Attack and Expert (my pick); add Harassment, which doubles Confuse Ray and pushes Toxic Spikes ahead of Stealth Rock but reads no harder (64); or add Prioritize Extremes, which reads easier (70)?
5. Saturn's theme line in [boss-shapes.md](boss-shapes.md) says "slow giants", which this draft is not: write Saturn 1's line as poison and hazards and keep the HQ fight's permanent Trick Room (my pick), or keep the line as it stands for both fights?
6. Name Saturn 1 for a spot-check reading? No, if decisions 1 to 3 take my picks, since the probe then puts him among fights the scorer read at 82 to 89 percent won (my pick); yes, if the draft stays as it is, to see whether a probe of 62 is under the 95 percent ceiling.

**Next steps.**

| Step | Who | Time |
|---|---|---|
| Answer the six questions, a line each | Ian | 10 minutes |
| Apply the answers on this branch, rerun legality, the lint, the tests and the probe | a session | about 45 minutes |
| Land the branch | the Overseer | 15 minutes |
| A spot-check reading, only if Ian names one | the scorer | two and a half to four hours |

Every pick is legal at its level on both checkers and keeps items and natures clear of repeats: with decisions 1 to 3 taken, the items are Focus Sash, Leftovers, Life Orb, Yache Berry, Babiri Berry and Poison Barb, and the natures Hasty, Bold, Rash, Mild, Timid and Modest.

## How Saturn 1 reads against the split

Each cell is the player's wins in 150 rough fights against the matchup screen's best six, then against the six it takes most; one number means the two were the same six. The player is the greedy probe player of the earlier checks, who never switches, never sets up and holds no items, so only the comparison between rows means anything. Fewer wins means a harder fight. Every row ran today on this branch. The old Saturn 1, Candice and Hesperid 1 as landed match their earlier pages' numbers exactly, so the harness reads as those did. Mars 2's row is her team after Ian's edit, and Cyrus 1's is his shape C, which the scorer read at 85, 85 and 76 percent won (82 overall).

| Fight, on its own boxes | Box 1 | Box 2 | Box 3 | Mean | Screen's best score, by box |
|---|---|---|---|---|---|
| Cyrus 1, shape C (47), for scale | 7, 2 | 3, 9 | 1, 0 | 4 | 11.65, 11.55, 10.85 |
| Saturn 1, the old team (53) | 40 | 29 | 28, 40 | 34 | 19.10, 17.95, 17.80 |
| Candice (56), in the gym's hail | 43, 37 | 51, 56 | 48, 54 | 48 | 17.55, 21.05, 20.05 |
| Hesperid 1, as landed (53) | 85, 60 | 66, 87 | 62, 66 | 71 | 21.70, 21.20, 21.85 |
| Mars 2, after Ian's edit (54) | 93, 114 | 42, 67 | 67, 42 | 71 | 16.50, 16.80, 16.65 |
| Saturn 1, Ian's draft (53) | 96, 46 | 67, 59 | 51 | 62 | 19.80, 19.50, 19.75 |

The picks, each swapped into the draft in memory with the other members as Ian built them:

| Saturn 1 with | Box 1 | Box 2 | Box 3 | Mean | Screen's best score, by box |
|---|---|---|---|---|---|
| 1a. Babiri Berry Azelf | 51, 49 | 59, 38 | 39, 40 | 46 | 18.80, 18.50, 18.75 |
| 1b. Shuca Berry and Naive Glimmora, Azelf keeps the Sash | 87, 46 | 74, 56 | 58, 54 | 62 | 19.80, 19.50, 19.75 |
| 1a with Naive Glimmora | 50, 46 | 65, 52 | 39, 38 | 48 | 18.80, 18.50, 18.75 |
| 2a. Rash Naganadel | 80, 42 | 26 | 44, 34 | 42 | 18.80, 19.50, 18.60 |
| 1a and 2a | 38, 26 | 26 | 35, 27 | 30 | 17.80, 18.50, 17.60 |
| 3a. Drain Punch Azelf | 33, 13 | 47, 31 | 31 | 31 | 18.80, 18.50, 18.75 |
| 3b. Dazzling Gleam Azelf | 92, 35 | 63, 52 | 52 | 58 | 19.80, 19.50, 19.75 |
| 1a, 2a and 3a | 29, 16 | 21, 14 | 12, 19 | 18 | 16.80, 18.20, 17.15 |
| Earth Power Glimmora, for Energy Ball | 94, 50 | 62, 68 | 46, 56 | 63 | 19.50, 19.20, 19.45 |
| Mud Shot Glimmora, for Energy Ball | 102, 59 | 64, 44 | 64 | 66 | 19.80, 19.60, 19.75 |
| 1a, 2a and Earth Power Glimmora | 51, 41 | 37, 22 | 29, 42 | 37 | 17.35, 18.50, 17.30 |
| The draft with Harassment | 89, 58 | 67, 53 | 59 | 64 | 19.80, 19.50, 19.75 |
| The draft with Prioritize Extremes | 97, 66 | 70, 60 | 63 | 70 | 19.80, 19.50, 19.75 |

How far to trust this, from [probe-ranking.md](probe-ranking.md): the probe gets the two ends right and the box order inside a fight right, but it does not order fights within about 35 wins of each other, and it cannot turn a probe number into a percent won. So the draft's gap to the old team (28 wins), to Candice (14) and to Hesperid and Mars (9) are all inside the blur: what can be said is that the draft is no longer clearly the split's hardest fight. The three picks together (18) are 44 wins harder than the draft, beyond the blur, and still 14 wins easier than Cyrus 1, whose shape C read 82 percent won. Fights at 11 to 45 on the probe read 86 to 89 percent won when the scorer read them (Jupiter 1's earlier team, Gardenia, Roark), Mars 1's earlier team at 9 read 58, and Somnu 1 at 81 read 94. The probe's greedy player never plays round status or hazards and never switches, so a team whose danger is poison and hazards reads harder here than a careful player finds it, and Dragon Tail and Confuse Ray cost the probe player more than they would cost a player who switches. That bias runs the same way across the rows above, so the comparison between them holds better than the absolute numbers.

## Part 1: what could invalidate the fight

### The rules

| Member | Level | Item | Nature | Ability (slot) | Speed in battle |
|---|---|---|---|---|---|
| Glimmora | 52 | Focus Sash | Hasty | Toxic Debris (1) | 121 |
| Mantine | 52 | Leftovers | Bold | Water Absorb (2) | 93 |
| Naganadel | 51 | Life Orb | Hasty | Beast Boost (1) | 158 |
| Tropius | 52 | Yache Berry | Mild | Overgrow (1) | 74, 148 under Tailwind |
| Azelf | 51 | Focus Sash | Timid | Levitate (1) | 151 |
| Salazzle (ace) | 53 | Poison Barb | Modest | Corrosion (1) | 145 |

Every level is under the cap of 56, and Salazzle is the ace at 53, as Ian set. Two rules break: the Focus Sash appears twice and Hasty twice (decisions 1 and 2). Nothing else does. No one-hit KO move, no evasion move, no trap and no trade move; the named Galactic fights are mostly anything goes in any case. A Life Orb is barred only for the player. Azelf in Oxide is Psychic and Fairy, with 600 base stats, and Naganadel has 540; weighed by their stats, as the ruling on legendaries asks, both sit with the ordinary pseudo-legendaries a commander may carry, and Azelf is the lake guardian Saturn has just taken.

The trainer lint finds nothing on the file; it does not look for repeats.

Legality. The OxiDex's lists and the Kaizo study's checker (with the TMs from before the TM pass) both read the file.

| Member | Move | Where it was | Now |
|---|---|---|---|
| Mantine 52 | Hurricane | on no Oxide list (a TM in the latest game) | Mantyke's egg list |
| Tropius 52 | Dragon Tail | on no Oxide list (a TM in the latest game) | Tropius's egg list |
| Tropius 52 | Tailwind | on no Oxide list (a tutor move in Platinum) | Tropius's egg list |

Both checkers then find nothing: the OxiDex's lists give all 24 moves at their levels, and the Kaizo checker finds 0 problems.

### The engine, the simulator and the AI

Each piece was read in the move data, the engine, the AI script and the simulator, and counted in the probe. The counts are per six over 150 fights.

- Toxic Spikes poisons a grounded Pokemon coming in, badly with two layers; Flying types, Levitate and Steel types are immune, and a grounded Poison type clears them. Toxic Debris lays a layer whenever a physical hit damages Glimmora, two at most. Both run in the engine and the simulator (the simulator's Toxic Debris since 2026-10-20). The player's Pokemon were poisoned coming in 220 to 463 times.
- Venoshock and Hex are 65 power, doubled into a poisoned target (Venoshock) or one with any status (Hex), in the engine and the simulator alike. Expert scores both by the target's state (`Expert_Venoshock`, `Expert_Hex`): plus 1 into a poisoned or statused target, minus 1 into a resist. Naganadel's Hex went into a poisoned target 32 to 113 times and its Venoshock 17 to 66, 49 to 148 between them, and the two went into a target with no status 2 to 23 times. Steel types are immune to Venoshock and, in Oxide's chart, resist Hex, so the box's Steel core is untouched by the payoff.
- Corrosion lets Salazzle's Toxic poison Steel and Poison types, in the engine, the simulator and the AI's poison check (`Basic_CheckCannotPoison`, since 2026-10-29). Toxic is a rare pick, 6 to 18 times, because Evaluate Attack and Expert favour Fire Blast; 3 to 11 of those went into a Steel or Poison type. Toxic Spikes themselves do not pass Corrosion's rule: a Steel type still ignores them.
- The Focus Sashes hold one hit from full HP, in both. Glimmora's held a hit 24 to 53 times and Azelf's 37 to 51. Hazards on the trainer's side break a Sash on entry, but the probe player almost never lays them, so neither Sash was broken that way; in play a player with Stealth Rock breaks Azelf's whenever it comes in (Levitate keeps Spikes off it). Glimmora, as the lead, never meets the player's hazards before its first hit.
- The Life Orb raises Naganadel's hits by 30 percent and costs it a tenth of its maximum HP each time. It cost Naganadel 27 to 34 times its maximum HP over 150 fights, and it fainted to its own Life Orb 7 to 31 times.
- Beast Boost raises its holder's highest stat a stage after each knockout, in both. Hasty makes Naganadel's Speed (158) higher than its Sp. Atk (150), so every raise went to Speed, 105 to 154 times, where Naganadel already outspeeds every Pokemon the box takes. With Rash its Sp. Atk is the highest (165), every raise went to Sp. Atk (200 to 301), and it knocked out 224 to 333 of the player's Pokemon instead of 130 to 166.
- Apple Acid is 90 power and always lowers the target's Sp. Def a stage, in both: 45 to 128 drops.
- Dragon Tail is 60 power at priority minus 6, and drags the target out for a random party member, who meets the hazards as it comes in (the simulator since 2026-10-15). Expert's force-switch rule (`Expert_ForceSwitch`) takes 3 from it unless hazards are down or the target has been in more than three turns, so it is picked once Glimmora has laid them: 65 to 106 uses, 39 to 73 drags, the Pokemon dragged in losing HP to the hazards 35 to 64 times and poisoned 17 to 35. It cannot touch a Fairy type.
- Tailwind doubles its side's Speed for the turn it is used and the two after (the engine's two-bit counter, and the simulator's 3), and the AI refuses it while it is up (`Basic_CheckTailwind`). It has 1 PP, by the setup rule. Tropius used it 27 to 58 times; Tropius made most of the attacks under it (19 to 52), and outsped 9 to 38 times a Pokemon it would not otherwise have outsped. The faster members gained almost nothing from it.
- Confuse Ray confuses, and a confused Pokemon hits itself half the time, in the engine and the simulator alike (the Generation 4 chance). Aqua Ring heals a sixteenth at each turn's end, with Leftovers beside it. Mantine confused its target 57 to 81 times and set Aqua Ring 91 to 123 times; the AI refuses a second Ring (`Basic_CheckAquaRing`).
- Nasty Plot raises Sp. Atk two stages and has 1 PP. Expert (`Expert_StatusSpAttackUp`) favours it at full HP, so Salazzle used it 80 to 99 times, mostly on coming in after a knockout, and 22 to 43 of its Fire Blasts came with the raise.
- Hurricane is 110 power at 80 accuracy in Oxide's move table (the base ROM's value, which stays), with a 30 percent chance to confuse. Toxic and Dragon Tail are at 100 accuracy there.

### The AI flags

Ian's flags are Basic, Evaluate Attack and Expert. By the guide ([battle-ai/flags-guide.md](battle-ai/flags-guide.md)):

- Check HP serves trade moves, setup and healing timing. The team has no trade move, and Expert already times Nasty Plot, Synthesis and Aqua Ring by HP, so it is left off.
- Harassment lifts only the moves in its table. Toxic Spikes and Confuse Ray are in it; Toxic and Stealth Rock are not. So it would not touch Salazzle's Toxic. With it, Mantine used Confuse Ray about twice as often (121 to 183 times) and Glimmora opened with Toxic Spikes in 84 to 106 fights of 150 rather than 54 to 65, at the cost of its Stealth Rock. The fight read no harder (64).
- Prioritize Extremes lifts every move the damage check skips: here all nine status moves, Stealth Rock and Toxic Spikes among them. With it Glimmora laid both hazards a little more often, Tailwind came 83 to 113 times and Nasty Plot 108 to 123, but the fight read easier (70), since those turns came at the cost of attacks. The guide keeps it off a team whose status moves are pieces of an attacking plan, which this is: Naganadel carries none, and the hazards and the Toxic serve the Venoshock and Hex payoff.
- Weather and Risky have nothing to serve, and Setup First Turn's table holds none of Glimmora's moves, the lead's.

So I would keep the three flags (decision 4).

## Part 2: each member's job

| Member | Its job | What it did, per six over 150 fights | Knocked out while it was in |
|---|---|---|---|
| Glimmora | the lead: lay both hazards behind the Sash | Toxic Spikes 117 to 134, Stealth Rock 104 to 126; opened with one of them in 109 to 135 fights of 150; Sash held 24 to 53 | 34 to 83 |
| Mantine | stall and confusion with Aqua Ring and Leftovers | Hydro Pump 208 to 272, Confuse Ray 58 to 81, Aqua Ring 91 to 123; the first member in after the lead in 69 to 112 fights | 72 to 138 |
| Naganadel | the payoff on poisoned targets | Hex and Venoshock into a poisoned target 49 to 148; Thunderbolt and Flamethrower for the rest; Life Orb faints 7 to 31 | 130 to 166 |
| Tropius | phaze into the hazards, and Tailwind | Dragon Tail drags 39 to 73, Apple Acid 182 to 252, Tailwind 27 to 58 | 154 to 170 |
| Azelf | the guardian: a fast attacker behind the Sash, and a second setter | Fire Blast 223 to 354, Psychic and U-turn the rest; Stealth Rock 20 to 42 | 130 to 175 |
| Salazzle | the ace: Nasty Plot and Fire Blast, Corrosion's Toxic for the Steel walls | Nasty Plot 80 to 99, Fire Blast 192 to 230, Venoshock into a poisoned target 7 to 29, Toxic 6 to 18 | 124 to 152 |

Glimmora does its job, and its few knockouts are not a fault: a lead whose job is the hazards scores low on that count however well it does it (Ian, 2026-11-01). Tropius does its job and makes the most knockouts. Naganadel and Salazzle make their knockouts, but Naganadel's Beast Boost is wasted on Speed (decision 2). Mantine does its stall job, but the AI's replacement rule spends it against Bastiodon and Probopass, which it loses to narrowly. Azelf hits hard, and its Stealth Rock is idle once Glimmora has laid the rocks (decision 3).

## Part 3: the weakest crux, Bastiodon

Bastiodon (Speed 44, Solid Rock, Rock Blast, Hard Press, Bulldoze and Taunt) is in 15, 20 and 20 of the screen's top 20 sixes on the three boxes, and by the screen it beats every member one on one: Glimmora by +2.5, Azelf by +2.5, Naganadel and Tropius by +1.5, Mantine and Salazzle by +0.5. Ian's lead test fails on it: as an answer to Glimmora it draws Mantine, which loses. Its best hits on Saturn's six are Rock Blast on Mantine, Tropius and Salazzle (96 to 150 percent) and Hard Press on Glimmora and Azelf (132 to 174). Saturn's best hits on it are Salazzle's Fire Blast (62 to 74), Mantine's Hydro Pump (63 to 73) and Naganadel's Thunderbolt and Flamethrower (42 to 50); Venoshock cannot touch it, and its Taunt stops Corrosion's Toxic.

The other common answers mostly pass the lead test: Quagsire (20 of 20 on box 1) beats Naganadel and Salazzle and draws Tropius, which beats it by 3.5; Corviknight, Metagross and Bronzong beat Glimmora and draw Salazzle with Nasty Plot, which beats them; Pachirisu beats Mantine and draws Azelf, which beats it.

The picks for the crux, each run through the screen, the replacement trace and the probe:

- Drain Punch in Azelf's Stealth Rock slot (3a) is the one that works. Azelf used it 174 to 271 times, and its knockouts rose to 158 to 243. Fighting is four times effective on Bastiodon and Probopass and twice on Garganacl and Empoleon, though Metagross, Bronzong and Corviknight take it at neutral. The fight reads 31 alone and 18 with decisions 1 and 2's picks. By the screen Azelf still loses to Bastiodon one on one (+1.5 rather than +2.5), but in play it draws back the HP it loses.
- Earth Power on Glimmora, for Energy Ball, makes the lead beat Bastiodon, so the lead test passes on every common answer of box 2. The screen still takes Bastiodon in 13 to 20 of its top sixes, as an answer to the other five, and the fight reads the same (63). It is also on no Oxide list for the line, so it would go on Glimmet's egg list.
- Mud Shot, Glimmora's level 27 move, is too weak to change anything (66).

## Part 4: the cheap checks

### Speed against the box

| Saturn 1 | Speed | Outspeeds | Is outspeeded by |
|---|---|---|---|
| Naganadel | 158 (144 if Rash) | every catch the screen takes | none (if Rash: Crobat 150, Talonflame 146) |
| Azelf | 151 | every catch the screen takes | none |
| Salazzle | 145 | all but two | Crobat 150, Talonflame 146 |
| Glimmora | 121 | Tentacruel 118, Pachirisu and Luxray 113, and the slow core | Crobat, Talonflame, Gengar 129, Delphox 123 |
| Mantine | 93 | Metagross 87, Corviknight 83, Empoleon 76 and the slow core | Altaria 97 and everything faster |
| Tropius | 74, 148 under Tailwind | Hippowdon 62, Probopass 55, Quagsire 50, Bastiodon 44; under Tailwind all but Crobat | everything from Empoleon (76) up, until Tailwind |

The goal 3 reference set at 53 (Crobat 150, Talonflame 146, Weavile 145, Greninja 142, Mienshao 124, Staraptor 124, Garchomp 121, Lucario 108) gives the same picture: Naganadel and Azelf outspeed all eight, Salazzle all but Crobat and Talonflame and ties Weavile, Glimmora only Lucario and ties Garchomp. Rash Naganadel at 144 falls under Crobat, Talonflame and Weavile.

### The matchup screen

The screen's best score is 19.50 to 19.80 by box, a little above the old team's 17.80 to 19.10, so the player's best six answers the draft a little better than the old team. Bastiodon is the core of every top six. Beside it the screen takes Quagsire and Garganacl on box 1, Pachirisu on boxes 2 and 3, and Hippowdon, Bronzong, Corviknight and Metagross by box.

### What the AI picks

| Member | What the AI picks most |
|---|---|
| Glimmora | Toxic Spikes and Stealth Rock first, then Energy Ball, then Sludge Wave; it switches out 24 to 52 times a six |
| Mantine | Hydro Pump, then Aqua Ring and Confuse Ray, Hurricane least (9 to 59) |
| Naganadel | Thunderbolt, Flamethrower or Hex by target, Venoshock least |
| Tropius | Apple Acid, then Dragon Tail once hazards are down, Tailwind and Synthesis |
| Azelf | Fire Blast, then Psychic and U-turn, Stealth Rock least |
| Salazzle | Fire Blast, then Nasty Plot, Venoshock, Toxic least |

## The egg-list commit

Commit 7c957e296c2 puts Hurricane on Mantyke's egg list and Dragon Tail and Tailwind on Tropius's own, under Ian's ruling of 2026-10-29, through `learnrewrite.IAN_EGG_MOVES` and the two species files, each species named once. Tropius's lists are set by hand, so its file holds the moves as well, and the generator's egg lists for both species agree with their files. No level-up entry moved, and the player never reaches an egg list. The draft itself is commit 5f8859e972e, saved through `trainers.save` and equal to the snapshot.

## How the numbers were made

Every number comes from the worktree `.claude/worktrees/saturn1-check` on this branch, cut from `origin/oxide` at 9447ef458e1. The scripts are the Hesperid check's, copied to `/home/ian/.claude/jobs/382760ce/tmp/saturn1-check/` and pointed at this worktree; none writes to `res/`. `bc.py` is the harness: `CAND=old` swaps the old team back in, `CAND=name` swaps a pick from `cands.py`, and `AIBITS` with `AISTEMS` swaps the flags. `checks.py FIGHT PLACE SEED` runs the screen, the replacement trace, damage both ways and the probe: 150 rough fights against the screen's best and its most-taken six. For this check it also counts Venoshock and Hex by the target's status, Toxic into Steel and Poison types, Apple Acid's drops, Dragon Tail's drags with the hazards met by the Pokemon dragged in, the Life Orb's cost and faints, each Beast Boost raise, attacks under Tailwind, each Focus Sash that held a hit or met hazards on entry, and the player's Pokemon poisoned or hurt coming in. `bait.py` is Ian's lead test, and `table.py` and `gather.py` made the tables, each range running over every six of the three boxes. `runall.sh` ran every job under `tools/oxide/capped`, with `free -g` showing 18 to 19 GB available. The boxes come from `plgoal3.setup` with the fresh run name `saturn1-check-study`, seeds 1 to 3, each fight on its own boxes: Saturn 1 and Hesperid 1 at 53, Mars 2 at 54, Candice at 56, Cyrus 1 at 47.

Checked on this branch: the trainer lint finds nothing; the real packer packs the file; both legality checkers find no off-list move; test_b1 passes 50 of 50, test_learnrewrite 6 of 6, test_learncheck 18 of 18 and test_trainers 44 of 44; `make rom` builds. The gate (`integrate.sh --verify-only`) passes 53 checks with no warning and fails only sync-docs, which refuses to mirror from any branch but `oxide`, by design.

Where the cheap checks' bias bites here: the screen counts only a clean one-on-one from full HP, with no status, no hazard and no Tailwind, so it cannot see the team's main idea. The probe player never switches, so it never plays round Toxic Spikes by leading with a Poison or Steel type, never uses Rapid Spin or Defog, almost never lays its own Stealth Rock to break Azelf's Sash, and stays in while confused.

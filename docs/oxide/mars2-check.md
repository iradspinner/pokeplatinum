# Mars 2: a check of Ian's first draft

Ian drafted Mars 2's new six in the OxiDex on 2026-11-01. She is fought at Lake Verity in Candice's split, after the Somnu and Moira double, with her ace at 54 (`candice-split.md`). He asked for the check his Maylene and Byron drafts had (`maylene-redesign.md`, `byron-brains-check.md`): anything that invalidates the fight, the weakest crux with the top picks for it, and the cheap checks. The draft is saved on branch `overseer-mars2-check` as Ian's first draft, kept on its branch for his check. The only other change is the egg-list commit for its two off-list moves. No team change was made, no scorer reading was run, and the simulator was not touched.

## Summary

**Outcome.** Nothing breaks the fight. Every move, item and ability does what the set means, in the engine and in the simulator alike, Oxide's reworked Giga Impact and one-turn Dig included. Two moves were off-list: Incineroar's Thunder Punch and Galarian Zapdos's Howl. Each is now on its line's first stage's egg list, Litten's and Galarian Zapdos's own. No item and no nature repeats, Purugly is the ace at 54 and the other five sit at 52 and 53 as Ian set them.

The AI does pivot, but mostly with two of the six pivot moves. Liepard's U-turn comes 67 to 94 times a six, and Incineroar's Parting Shot 86 to 149, nearly always into a target above 70 percent HP, mostly one the user outspeeds. Liepard's U-turn brings in Galarian Zapdos, which beats the Pokemon in front in most switches. The other three U-turns come 0 to 68 times a six, and their switches mostly bring in a member that loses, because by then nothing on the bench wins. Check HP has no exploder to steer here; it only times Howl, keeps Roost back at high HP and keeps Thunder Wave off a nearly beaten target. That is harmless, so I would keep it.

On the cheap checks the draft reads no harder than the team it replaces. The probe's player wins about 90 fights of 150 against either, where Saturn 1 is held to about 34, Cyrus 1 to 40 and Candice to 48. The matchup screen reads the draft as the split's hardest fight, because its members win one-on-ones from full HP. The probe shows those wins leaking away in play: recoil from Giga Impact (the ace faints to its own recoil in 17 to 36 fights of 150), Brave Bird and Flare Blitz, Parting Shot turns that deal no damage, and two members that the box's Steel and Rock core walls. On the probe-ranking's evidence a fight at about 90 sits with Maylene and Somnu 1. Cyrus 1, held to 40 on the probe, read 98 percent won on the scorer, so this draft would likely read at or above the 95 percent ceiling for a boss.

**The weakest crux is Crobat's slot**, with Mesprit's beside it. Crobat knocks out 28 to 38 of the player's Pokemon per 150 fights, against 64 to 280 for the rest. Both its attacks are resisted or blocked by the box's core (Golem, Bastiodon, Probopass, Metagross), so new Crobat sets change nothing. The lead's own weakness is Staraptor, in 15 to 20 of the screen's top 20 sixes on two boxes: it beats Liepard and draws Incineroar, which loses to it. Luxray, the old team's ace, fixes that wherever it goes, since Staraptor then draws Luxray. Put in Mesprit's slot, it keeps Mars's canon bat, and Crobat then makes 61 to 158 knockouts a six, because it is drawn in against the Fighting and Fairy answers it beats. The fight then reads about as Byron does.

### What Ian decides

1. Mars 2's weakest crux: Luxray in Mesprit's slot, so the fight reads about as Byron does and keeps the bat (my pick); Luxray in Crobat's slot, harder again, about as Candice reads, but without the bat; Meowscarada in Crobat's slot, about as hard as Saturn 1; or keep the draft, which reads as easy as the old team?
2. Mars 2's AI flags: keep Basic, Evaluate Attack, Expert and Check HP (my pick), or drop Check HP, which has no exploder to steer here?
3. Thunderous Kick has no contact flag in Oxide's move table, where the later games make it contact: add the flag (my pick, a one-line data fix in its own commit), or leave it?
4. Name Mars 2 for a spot-check reading? No if decision 1 takes one of its picks, since each puts her among the split's other bosses on the probe (my pick); yes if the draft stays, to see whether it reads above the 95 percent ceiling.

**Next steps.** Ian answers in a line each, about ten minutes. A session then applies his choices on this branch and reruns the legality checks, the lint, the tests and the probes, about 45 minutes; Luxray's set is already legal at 52 and at 53 on both checkers. Hesperid's check is on its own branch beside this one. A spot-check reading, if Ian names one, takes two and a half to four hours of machine time.

## What could invalidate the fight

### The rules

| Member | Level | Item | Nature | Ability (slot) | BST |
|---|---|---|---|---|---|
| Liepard | 53 | Focus Sash | Adamant | Prankster (2) | 496 |
| Crobat | 53 | Sharp Beak | Jolly | Infiltrator (hidden) | 535 |
| Incineroar | 53 | Sitrus Berry | Impish | Intimidate (hidden) | 530 |
| Galarian Zapdos | 52 | Black Belt | Lonely | Defiant (1) | 580 |
| Mesprit | 52 | Starf Berry | Timid | Magic Guard (1) | 600 |
| Purugly (ace) | 54 | Silk Scarf | Naughty | Thick Fat (2) | 492 |

No item repeats and no nature repeats. Purugly is the ace at 54 and the rest are under it, as Ian set. Mars is a commander, so a boss, and the named Galactic fights are mostly anything goes so long as they are fun and thematic (`boss-shapes.md`). The draft carries no one-hit KO move, no evasion move, no trap and no trade move. Its theme is "mostly cats, with her canon bat": Liepard, Incineroar and Purugly are cats and Crobat is the bat; Mesprit is the lake's own legendary and Galarian Zapdos the one member outside the theme. The Focus Sash sits on a lead with no trade move, the case Ian kept on Darach's lead and Argenta's.

Galarian Zapdos raises nothing the rules care about. Weighed by its base stat total (580) and its role, as a Salamence or a Goodra would be (600 each), it is the team's second-strongest member on paper, below Oxide's Mesprit (600), and it is the member the lead's answers draw. It makes 169 to 227 knockouts a six, second only to Incineroar.

Legality. Two checkers read the file: the OxiDex's own lists, which read today's TMs, and the Kaizo study's checker at 54, which counts the TMs from before the TM pass. Both failed the same two moves, and both pass every move now.

| Member | Move | Where Oxide had it | Egg list |
|---|---|---|---|
| Incineroar 53 | Thunder Punch | nowhere (a TM in the latest game) | Litten |
| Galarian Zapdos 52 | Howl | nowhere | Galarian Zapdos, a first stage of its own |

Each is in `learnrewrite.IAN_EGG_MOVES`, Litten's under its one existing entry, so each species is named once, and the generator's output agrees with both files.

### The moves, the items and the abilities

Each was read in the move and item data, the engine and the simulator. All of them run in both.

- Giga Impact is Oxide's rework: 180 power, no recharge turn, half the damage dealt as recoil. With Purugly's Silk Scarf it takes 175 to 207 from a box Staraptor.
- Dig is one turn, a plain 60-power Ground hit with no turn underground. It is Purugly's answer to Steel, 48 to 63 on Bastiodon and Probopass, where Giga Impact does 19 to 27.
- Thunderous Kick is 90 power and lowers Defense a stage on every hit. Oxide's move table gives it no contact flag, though the later games make it contact, so contact abilities and a Rocky Helmet never touch Galarian Zapdos for it (decision 3).
- Darkest Lariat, 85 power, ignores the target's stat stages in the engine and the simulator alike, so an Iron Defense Metagross takes it in full.
- Throat Chop's sound block runs in both since the simulator fixes of October.
- Parting Shot lowers the target's Attack and Sp. Atk a stage, then switches its user out; it fails, and its user stays in, when both stats are already at -6. Each return brings Incineroar's Intimidate again.
- Fake Out has +3 priority and works only on its user's first turn out. Liepard opens with it, and Purugly uses it on coming in (122 to 132 a six). It fails on the Ghost Rotom, which boxes 2 and 3 take, and Liepard then opens with Throat Chop.
- Prankster gives Liepard's Thunder Wave +1 priority, and fails into a Dark type in the engine, the simulator and the AI alike. Its Thunder Wave landed 58 to 73 times a six.
- Defiant raises Galarian Zapdos's Attack two stages when the player's Intimidate or any drop hits it.
- Magic Guard spares Mesprit hazard, recoil, poison and weather damage. The Starf Berry raises a random stat two stages at a quarter HP; it was eaten 46 to 93 times a six.
- The Focus Sash held 8 to 52 times a six, fewest on box 3.
- The Sharp Beak, Black Belt and Silk Scarf each raise their type's moves by a fifth, and each holder's main attack is of that type. Thick Fat halves Fire and Ice into Purugly, and Infiltrator lets Crobat pass screens and a Substitute.

### The AI and the pivots

Expert scores U-turn (`Expert_UTurn`) and Parting Shot alike: minus 1 into a resist (U-turn only), minus 2 at 75 percent if the user has a super-effective attack, minus 2 at 75 percent if no bench member hits harder, then plus 1 or 2 against a target above 70 percent HP, and plus 1 if the user is faster. U-turn is also a damaging move, so Evaluate Attack takes 1 from it whenever another attack is stronger. Parting Shot is a status move, so it keeps its starting score, and against a healthy target it often wins.

| Pivot, per six of 150 fights | Picks | Switches that brought in a member that beats the Pokemon in front | Lost, with a winner on the bench | Lost, with no winner on the bench |
|---|---|---|---|---|
| Liepard's U-turn | 67 to 94 | 35 to 63 | 0 to 3 | 1 to 34 |
| Incineroar's Parting Shot | 86 to 149 | 21 to 93 | 8 to 24 | 22 to 47 |
| Mesprit's U-turn | 22 to 68 | 0 to 3 | 0 to 1 | 9 to 24 |
| Galarian Zapdos's U-turn | 0 to 53 | 0 to 18 | 0 to 5 | 6 to 26 |
| Crobat's U-turn | 6 to 17 | 0 to 6 | 0 | 3 to 10 |

"Beats" is the matchup screen's one-on-one margin, so it is a rough guide. The rest of each row is switches into a fainted Pokemon's slot, or a U-turn with no switch after it (the user was the last one standing, or the hit ended the fight). Liepard's and Incineroar's picks came nearly all against a target above 70 percent HP (364 of 387 and 475 of 547 over the five sixes), almost always with the user the faster. Mesprit's and Crobat's were spread over every HP band. Liepard's U-turn is its first-turn move in 27 to 55 fights of 150 and Fake Out in 70 to 123.

The replacement after a pivot is the same rule as after a knockout (`BattleAI_PostKOSwitchIn`, from `BattleAI_SwitchedSlot` when no switch was planned), and the simulator runs it the same way. It first takes the member whose types score best against the Pokemon in front and that has a super-effective move on it, so against the box's Rock and Steel core it brings Galarian Zapdos. That is what the team wants. When the rule's pick loses, there was usually no winner on the bench to take.

### The AI flags

Mars 2 runs Basic, Evaluate Attack, Expert and Check HP. With no Explosion, Self-Destruct or Destiny Bond on the team, Check HP does three small things here, each by its tables in the script (`CheckHP_Main`). It takes 2, at 80.5 percent, from Howl when Galarian Zapdos is at 70 percent HP or less, and again when its target is, so Howl comes only from a healthy Zapdos against a healthy target (picked 68 to 104 times a six). It takes 2 from Roost above 70 percent HP, which Expert already refuses. And it takes 2 from Thunder Wave into a target at 30 percent HP or less, where a hit is better. None of this works against the team, so I would keep it (decision 2). The other flags have no idea to serve: Harassment wants a status team, and two Thunder Waves are not one; Risky wants a critical-hit team; Weather wants a weather lead; Prioritize Extremes would push more Parting Shots, which the AI already picks often.

### Where the simulator falls short

The mechanics above all run, and none of the verified gaps (`simulator-gaps.md`) still open touches this team. The shortfalls are the probe's. Its greedy player never switches, sets nothing up and holds no items. So Stealth Rock (69 to 120 a six) bites only after a knockout, the Attack drops from Parting Shot and Intimidate stay on a player who in play would switch them off, and a Pokemon that Fake Out flinches is never pulled out. The matchup screen counts only a clean one-on-one from full HP, so it sees no recoil, no status, no hazard and no Fake Out. Both read only the comparison between rows.

## The fight against the boxes

The player's Pokemon knocked out while each member was in, per six of 150 fights, over the five sixes on Mars 2's boxes (goal 3's boxes at her ace of 54):

| Liepard | Crobat | Incineroar | Galarian Zapdos | Mesprit | Purugly |
|---|---|---|---|---|---|
| 41 to 101 | 28 to 38 | 183 to 280 | 169 to 227 | 70 to 156 | 64 to 93 |

The old team, for comparison: Mesprit 48 to 79, Crobat 67 to 147, Bronzong 115 to 218, Purugly 42 to 82, Umbreon 120 to 168, Luxray 102 to 223.

Recoil is where the screen's wins leak away. Purugly's Giga Impact, picked 176 to 238 times a six, costs it 22 to 31 times its maximum HP over the 150 fights, and the ace faints to its own recoil in 17 to 36 of them. Crobat's Brave Bird costs it 9 to 13 times its maximum HP and faints it 4 to 12 times, and Incineroar's Flare Blitz, net of its Sitrus Berry, 6 to 41 times and 2 to 14 faints. Purugly's 64 to 93 knockouts are few for an ace. Its Giga Impact into the Steel walls does 19 to 60, so the AI's strongest move is often a small hit that still costs HP.

### Speed against the box

Speeds in battle: Crobat 174, Liepard 144, Purugly 142, Galarian Zapdos 125, Mesprit 114, Incineroar 85. The box's most-taken catches, by how many of the screen's top 20 sixes take them:

| Box | Catches (Speed, sixes of 20) |
|---|---|
| 1 | Staraptor (126, 20), Golem (61, 20), Bastiodon (45, 14), Probopass (56, 13), Metagross (88, 13) |
| 2 | Bastiodon (45, 20), Golem (61, 17), Staraptor (126, 15), Rotom (111, 9), Rhydon (56, 9), Empoleon (77, 8), Bronzong (48, 7) |
| 3 | Golem (61, 20), Rotom (111, 20), Bastiodon (45, 20), Metagross (88, 7), Bronzong (48, 6), Empoleon (77, 5) |

Crobat outspeeds everything the screen takes, the box's own Crobat (153) included. Liepard and Purugly outspeed all but that Crobat. Galarian Zapdos, at 125, is one point under Staraptor and ties Delphox; Mesprit is three points over Rotom. Incineroar outspeeds the slow core but not Metagross.

### The lead test

Ian's test (2026-10-29): a lead may be wholly countered if each answer draws in a member that beats it, best with a setup move. Liepard's common answers on all three boxes are the Rock and Steel core and Staraptor. Golem, Bastiodon, Probopass, Rhydon, Empoleon and Garganacl each draw Galarian Zapdos, which beats them and carries Howl. Two answers fail the test. Staraptor (+1.5 on Liepard, in 20 of the top sixes on box 1 and 15 on box 2) draws Incineroar, which loses to it (+0.5), and Metagross (+2.5) draws Incineroar, which loses too (+0.5). Staraptor also beats Galarian Zapdos, Incineroar and Mesprit one on one; only Purugly and, narrowly, Crobat beat it.

## The weakest crux: Crobat's slot

Crobat makes the fewest knockouts, 28 to 38 a six. It picks Brave Bird 178 to 260 times a six, mostly into Golem, Bastiodon, Probopass and Metagross (12 to 39 damage), and its Cross Poison does nothing to Steel. The replacement rule brings it in last, when what is left in front is what walls it. Mesprit has the same trouble: its Psychic does 15 to 26 to the Steel walls. The two together leave the fight to Incineroar and Galarian Zapdos.

Each pick keeps the other five as Ian built them, swapped into the slot in memory and run through the screen, the replacement trace and the probe on the same boxes. Items and natures stay clear of the other five; Luxray's set is the old team's, legal at 52 and 53 on both checkers.

| Pick | Lead test | Its knockouts a six | Box 1 | Box 2 | Box 3 | Mean of the three boxes |
|---|---|---|---|---|---|---|
| Ian's draft | fails on Staraptor and Metagross | Crobat 28 to 38 | 107, 79 | 97 | 87, 71 | 90 |
| 1. Luxray for Mesprit, Expert Belt, Hasty, Tinted Lens; Thunder Fang, Crunch, Superpower, Howl | passes on every common answer | Luxray 77 to 127, Crobat 61 to 158 | 63, 51 | 77, 94 | 63, 71 | 70 |
| 2. Luxray for Crobat, Expert Belt, Jolly, the same set | fails on Metagross only | Luxray 80 to 168 | 61, 54 | 73, 51 | 27, 39 | 51 |
| 3. Meowscarada for Crobat, Miracle Seed, Jolly, Overgrow; Flower Trick, Knock Off, Brick Break, U-turn | fails on Staraptor and Metagross | Meowscarada 129 to 215 | 26, 46 | 2, 10 | 27, 31 | 24 |
| Crobat with Hypnosis for Cross Poison | as the draft | Crobat 34 to 43 | 98, 78 | 92 | 87, 66 | 86 |
| Crobat with Heat Wave for Cross Poison | as the draft | Crobat 37 to 56 | 100, 73 | 97 | 85, 66 | 86 |

Pick 1 is my first. It keeps the canon bat and makes Crobat useful, since without Mesprit the replacement rule draws Crobat against the Fighting and Fairy catches it beats (Grapploct, Sylveon, Granbull). Luxray takes Staraptor, Empoleon and Corviknight, and Liepard's lead then passes on every common answer of every box. The fight moves to about Byron's level on the probe. The price is Mesprit, the lake's own legendary and the team's one Stealth Rock, and the second Thunder Wave. Pick 2 is harder still and keeps Mesprit, but drops the bat. Pick 3 makes Mars 2 about as hard as Saturn 1 and harder than Candice, and its lead still fails on Staraptor. New Crobat sets do nothing: Hypnosis puts a target to sleep 32 to 66 times a six and Heat Wave hits 116 to 203 times, yet neither moves the fight beyond the probe's spread.

## How Mars 2 reads against the split

Each cell is the player's wins in 150 rough fights against the screen's best six, then against the six it takes most; one number means the two were the same six. Fewer wins means a harder fight. Each fight is on its own goal 3 boxes. The rows for Mars 2's draft and old team, Saturn 1, Candice and Cyrus 1 were run on this branch after it took in Pursuit at 60 (9e96c3e00), and each matches the Candice split's numbers exactly, so the harness reads as that one did. Hesperid 1's and Byron's rows are that page's.

| Fight, on its own boxes | Box 1 | Box 2 | Box 3 | Mean | Screen's best score, by box |
|---|---|---|---|---|---|
| Saturn 1 (53) | 40 | 29 | 28, 40 | 34 | 19.10, 17.95, 17.80 |
| Cyrus 1 (47), for scale | 61, 29 | 44, 20 | 44, 44 | 40 | 17.30, 17.20, 17.70 |
| Candice (56), in the gym's hail | 43, 37 | 51, 56 | 48, 54 | 48 | 17.55, 21.05, 20.05 |
| Hesperid 1 (53) | 68, 59 | 67, 70 | 96, 52 | 69 | 20.25, 19.60, 19.60 |
| Byron (53), for scale | 69, 81 | 67, 81 | 41, 86 | 71 | 18.15, 18.60, 19.75 |
| Mars 2's old team (54) | 62, 43 | 90, 114 | 124, 99 | 89 | 21.15, 22.30, 21.00 |
| Mars 2, Ian's draft (54) | 107, 79 | 97 | 87, 71 | 90 | 16.95, 17.25, 16.80 |

How far to trust this, from `probe-ranking.md`. The probe gets the two ends right and fails in the middle: it does not order fights within about 35 wins of each other, and it cannot turn a probe number into a percent won. Fights under about 30 have read anything from 58 to 89 percent won. Mars 2's draft sits about 55 wins above Saturn 1 and 40 above Candice, far enough to say it is easier than both. Against the old team and Byron it is within the blur. Cyrus 1, at 40 here, read 98 percent won on the scorer, and Maylene (88) and Somnu 1 (81, 94 percent won) sit near the draft, so it would likely read at or above the 95 percent ceiling for a boss.

### Somnu and Moira

The officers come before Mars at the lake, as one double battle: Somnu's Swalot, Skuntank and Glaceon and Moira's Abomasnow, Mamoswine and Gardevoir, at 51, 51 and 52 each, three each, not yet redesigned. The probe plays single battles only, so the double cannot be read beside her. What can be said: every one of the six sits at or under Mars's lowest level (52, against her 52 to 54), and their base stat totals run 467 to 560, against her 492 to 600. Whether two of them at once read harder than Mars alone is beyond these checks; if Ian picks a harder Mars (picks 1 to 3), the gap only widens.

## How the numbers were made

Every number comes from the worktree `.claude/worktrees/mars2-check` on this branch, with the draft saved and the egg lists added. The picks and the first runs were made on `origin/oxide` at 57c418a6fe8, before Pursuit at 60 (9e96c3e00) reached it; the branch was then rebased onto 0db1aeaee9c, and the draft, the old team, Saturn 1, Candice and Cyrus 1 were run again there, each to the same numbers. No Pursuit appears on any Mars 2 row's teams or in the screen's top sixes for her boxes. The scratch scripts are in `/home/ian/.claude/jobs/382760ce/tmp/mars2-check/`, copied from the Candice split's checks and pointed at this branch, and none writes to `res/`.

- `bc.py` is the harness: goal 3's box for a place (run `mars2-check-study`, seeds 1 to 3) and any fight against it, in memory. `CAND=old` swaps the old team back in; `CAND=name` swaps a pick from `cands.py`.
- `checks.py FIGHT PLACE SEED [N]` runs the screen's top 20 sixes, the margins, the replacement trace, damage both ways, and the probe of 150 rough fights against the best and the most-taken six. For this check it also counts each pivot pick by the target's HP and the Speed order, what each pivot's switch brought in against the Pokemon in front, and each recoil move's HP cost to its user. `runall.sh` and `runcands.sh` run it under the memory cap; `summarise.py`, `bait.py` (the lead test) and `pivsum.py` gather the tables.
- Legality comes from the OxiDex's `learnsets.lists` and the Kaizo checker (`oxide.py check 54`, with `OXIDE_OLD_RES` set to the export of `res/` from before the TM pass).

Checked on this branch after the rebase: the trainer lint finds nothing; the save ran the real packer; both legality checkers find no off-list move; test_learnrewrite passes 6 of 6, test_learncheck 18 of 18, test_trainers 44 of 44 and test_b1 50 of 50; `make rom` builds. The gate (`integrate.sh --verify-only`) passes 53 checks with no warning and fails only sync-docs, which refuses to mirror from any branch but `oxide`, by design.

# Officer Hesperid 1: a short check of Ian's draft

Ian drafted Officer Hesperid 1's new six in his OxiDex on 2026-11-01. Hesperid is a named Galactic officer, a mini-boss, fought at Lake Valor before Saturn 1 in Candice's split (cap 56), with his ace at 53 as Ian ruled. His theme is Platinum Kaizo teambuilding with no holds barred, on rarely used Pokemon with odd movesets ([boss-shapes.md](boss-shapes.md)), and he is the one officer allowed to read harder than his commander. This is the check Maylene's six and the Brains had: anything that invalidates the fight, the weakest crux with the top picks for it, and the cheap checks. The draft is on branch `overseer-hesperid-check`, saved as it stands; the only other change to the game's data is the egg-list commit below. No scorer reading was run.

## Summary

**What could not be checked, first.** The simulator crashes on this team. When Chatot, whose ability is Scrappy, faints with a Ghost type in front, the trainer AI's replacement rule divides by zero (`fightai._ko_score`), so a scorer reading of this draft would stop on boxes 2 and 3. The probes below ran with a guard in my scratch harness that rescores that one case as Scrappy makes it; the simulator file was not changed, and the guard fired 7 to 29 times a six. Decision 5 asks for the fix. Nothing was seen in game.

**Outcome.** Nothing in the rules breaks the fight. No item or nature repeats, every ability is the one Ian picked, and three moves that were on no list at their levels are now on egg lists. Two pieces of the engine work against the draft's ideas, and both come from the AI's Baton Pass flag. Weezing, the lead, explodes on the battle's first turn in 80 to 97 fights of 150; into Bastiodon, the box's most common answer, that Explosion does 27 to 32 percent. Girafarig's Agility and Baton Pass do not chain: neither of the AI's Baton Pass routines looks at Speed, so it passes only when its Starf Berry has raised a second stat. On the probe Hesperid reads clearly easier than Saturn 1 and a little easier than Byron, and easier than his old team.

**The weakest crux is Sudowoodo's slot.** It knocks out 18 to 49 of the player's Pokemon per 150 fights, against 59 to 179 for the other five. Bastiodon, in all 20 of the screen's top sixes on every box, is its main target. Focus Punch is its only good hit on Bastiodon (120 to 144 percent), but it lands in 17 to 31 of its 65 to 109 uses, since the player hits first. Its other three moves get no damage comparison, so the Baton Pass flag lifts all four alike at high HP.

**What Ian decides.**

1. The Baton Pass flag: drop it (my pick), give Girafarig Calm Mind for Agility so the flag can read what it passes, or keep it?
2. Sudowoodo's slot: Magcargo with Shell Smash (my pick), Sudowoodo with Earthquake for Focus Punch, or keep Sudowoodo?
3. Hesperid's difficulty: with 1 and 2 taken he reads between Byron and Saturn 1. Stop there (my pick), push him past Saturn with another round of picks, or keep the draft's level?
4. Sceptile's item: a White Herb for the Yache Berry (my pick), so Unburden fires, or keep the Yache?
5. Approve a simulator fix for the Scrappy crash, with a test that fails before it (my pick: yes, before any reading of Hesperid)?

**Next steps.**

| Step | Who | Time |
|---|---|---|
| Answer the five questions, a line each | Ian | 15 minutes |
| Apply the answers on this branch, rerun legality and the probe | a session | about an hour |
| The Scrappy fix with its failing test, landing through the Overseer | a session, with Ian's yes | about an hour |
| A spot-check reading, only if Ian names one | the scorer | two and a half to four hours |

## How he reads against his commander

Each cell is the player's wins in 150 rough fights against the matchup screen's best six, then the six it takes most; one number means the two were the same six. The player is the greedy probe player of the earlier checks, who never switches, never sets up and holds no items, so only the comparison between rows means anything. Fewer wins means a harder fight. Every row ran today on this branch, at the tree with Pursuit at 60; Saturn 1's match the Candice pass's numbers exactly, and Byron's differ from them by 1 to 4 wins a cell.

| Fight, on its own boxes | Box 1 | Box 2 | Box 3 | Average | Screen's best score, by box |
|---|---|---|---|---|---|
| Saturn 1 (53) | 40 | 29 | 28, 40 | 34 | 19.10, 17.95, 17.80 |
| Byron (53) | 68, 80 | 66, 85 | 41, 90 | 72 | 18.15, 18.60, 19.75 |
| Hesperid 1, his old team (53), from the Candice pass | 68, 59 | 67, 70 | 96, 52 | 69 | 20.25, 19.60, 19.60 |
| Hesperid 1, Ian's draft | 123, 101 | 84, 108 | 101, 103 | 103 | 21.70, 21.20, 21.85 |
| The draft without the Baton Pass flag | 89, 64 | 74, 88 | 69, 72 | 76 | the same |
| The draft with Magcargo for Sudowoodo | 89, 79 | 87, 110 | 81, 97 | 91 | 21.40, 21.50, 22.15 |
| Magcargo and no Baton Pass flag | 51, 46 | 67, 87 | 47, 79 | 63 | 21.40, 21.50, 22.15 |

How far to trust this, from [probe-ranking.md](probe-ranking.md): the probe gets the two ends right and the box order inside a fight right, but it does not order fights within about 35 wins of each other, and it cannot turn a probe number into a percent won. A probe average near 80 has meant 94 percent won (Somnu 1), and one near 120 meant 100 (Moira 1). So the draft's gap of about 70 wins to Saturn 1 is real: as drafted, Hesperid is much easier than his commander. His gap to Byron, about 30, is inside the blur. The probe's greedy player never plays round status or setup, so a team whose danger is status or a sweep reads harder here than a careful player finds it; this team has little status, Stealth Rock and Perish Song apart, so that bias is small here.

## Part 1: what could invalidate the fight

### The rules

No item repeats (Black Sludge, Yache Berry, Starf Berry, BrightPowder, Silk Scarf, Choice Specs), and no nature repeats (Relaxed, Hasty, Jolly, Gentle, Quiet, Modest). The abilities, by slot: Weezing Levitate, Sceptile its hidden Unburden, Girafarig Quick Feet, Sudowoodo Sturdy, Wigglytuff Cute Charm, Chatot Scrappy. No one-hit KO, evasion or trapping move. The named Galactic fights may carry trade moves freely, and this one carries three: two Explosions and a Misty Explosion.

Three moves were on no list at their levels, by the OxiDex's reading:

| Member | Move | Where it was | Now |
|---|---|---|---|
| Sudowoodo 52 | Explosion | Sudowoodo's TM before the TM pass, so the Kaizo checker passed it | Bonsly's egg list |
| Sudowoodo 52 | Focus Punch | the same | Bonsly's egg list |
| Wigglytuff 52 | Misty Explosion | no Oxide list for the line | Igglybuff's egg list |

Both checkers then find nothing: the OxiDex's lists give all 23 moves at their levels, and the Kaizo checker (with the pre-TM-pass TMs) finds 0 problems. The trainer lint finds only its warning on the Choice Specs.

### The engine and the simulator

Each piece was read in the engine and, where it matters, counted in the probe.

- Explosion is 250 power and still halves the target's Defense, the Generation 4 rule, so it hits as if 500. Misty Explosion carries the same effect, but it is special and the halving reads Defense only, so it is a plain 200-power Fairy hit that faints its user. Oxide has no terrain, so it gains nothing there either. The simulator agrees: Wigglytuff's Misty Explosion does a little less than its Silk Scarf Hyper Beam into most targets.
- Hyper Beam is Oxide's version: 180 power, no recharge, half the damage as recoil. Wigglytuff picks it 186 to 332 times a six, with the Silk Scarf.
- Chatter is a plain 65-power Flying hit for a trainer: an AI's Chatot has no recorded cry, so it confuses one time in a hundred, in the engine and the simulator alike.
- Focus Punch is 150 power at priority minus 3 and fails if its user was hit first that turn. Sturdy (Oxide's Generation 5 version, which leaves a full-HP holder at 1 HP) keeps Sudowoodo standing, but the hit still breaks the focus.
- Unburden doubles Sceptile's Speed once its item is spent. A Yache Berry is spent only by a super-effective Ice hit, and against a Grass and Dragon type that hit knocked Sceptile out anyway: the berry went 0 to 15 times a six, and Sceptile never attacked with Unburden on. Decision 4.
- BrightPowder works in the simulator, which the Candice pass and this brief said it did not. The scorer's battle (`perfectline.accuracy_hits`) has cut accuracy by a tenth for its holder since 2026-09-30, and the engine does the same (`HOLD_EFFECT_ACC_REDUCE`). The probe counts it: 10 to 13 percent of the player's accuracy checks on Sudowoodo missed. The fightsim battle's own accuracy check lacks it, but the readings do not use that one.
- Choice Specs locks Chatot into its first move, in the engine and the simulator. On boxes 2 and 3 it picks Heat Wave 345 to 378 times a six, against the Steel walls, and stays locked. A Choice-locked trainer is weaker in play than its score, since the player picks the lock with a lead and switches to something immune; his theme allows Choice items, so this is information, not a fault.
- Pursuit is 60 power, doubled into a switching foe. The probe's player never switches, so here it is a plain 60-power Dark hit.
- The Starf Berry raises a random stat by two at a quarter of HP, and went 53 to 110 times a six.
- Scrappy lets Chatot's Hyper Voice hit Ghosts, which the damage rows count (115 to 136 percent on Dhelmise). It is also where the simulator crashes: `fightai._ko_score` divides the calculator's damage by the chart's effectiveness, which is 0 for Normal into Ghost even under Scrappy. Decision 5.

### The AI flags

Ian's flags are Basic, Evaluate Attack, Expert, Baton Pass and Check HP. Check HP is right for a team with trade moves ([battle-ai/flags-guide.md](battle-ai/flags-guide.md)): it holds Explosion back while the user is healthy, so it lands where the player can see it coming. The Baton Pass flag is the problem, as the Candice pass found, and here it matters twice.

First, its bug (O2 in [battle-ai/other-flags.md](battle-ai/other-flags.md)) lifts every move that gets no damage comparison: every status move, Explosion, Misty Explosion, Focus Punch and Sucker Punch. Such a move gains 3, then 5 more on the battle's very first turn, 1 more later at 60 percent HP or above, and loses 10 below 60 percent. For a team whose members do not know Baton Pass it runs 68.75 percent of the time. So on turn 1 Weezing's Explosion gains 8, which beats Check HP's 2 and Expert's 3, and Weezing explodes at once. Later it reverses Check HP: an exploder above 60 percent is pushed toward Explosion, one below 60 percent away from it.

| Weezing's Explosion, per 150 fights a six | With the flag | Without it |
|---|---|---|
| on the battle's first turn | 80 to 97 | 0 to 1 |
| at 30 percent HP or less | 3 to 5 | 16 to 34 |

Second, the flag does not serve Girafarig's chain. Its pass rows count only Attack and Sp. Atk stages, and Expert's Baton Pass routine counts Attack, both defences, Sp. Atk and evasion, never Speed. After Agility alone, Baton Pass scores 2 under Girafarig's attacks, so the AI keeps attacking at doubled Speed. It passed 31 to 73 times a six, and every pass in box 1's counts carried a stage the Starf Berry gives, with or without Agility's Speed beside it. Agility itself goes 93 to 115 times a six with the flag, because the bug lifts it by 4, and 1 to 10 times without the flag.

With Calm Mind in Agility's place, the pass rows read the Sp. Atk it raises: Girafarig used Calm Mind 82 to 135 times a six and passed 54 to 102 times, but the fight read about the same (90 to 109 wins). Without the flag the fight reads harder by about 27 wins a box, mostly because Weezing stops spending itself on turn 1, though Agility then falls nearly unused.

## Part 2: the weakest crux

### Sudowoodo's slot

| | Weezing | Sceptile | Girafarig | Sudowoodo | Wigglytuff | Chatot |
|---|---|---|---|---|---|---|
| Player's Pokemon knocked out while it was in, per 150 fights | 59 to 98 | 105 to 131 | 137 to 179 | 18 to 49 | 107 to 157 | 138 to 178 |

Sudowoodo is the first member in after the lead in 43 to 104 fights of 150, because the replacement rule sends it at Bastiodon and Probopass, which beat Weezing. The bait test mostly passes there, but narrowly: the screen gives Bastiodon a margin of minus 0.5 on Sudowoodo, and that rests on Focus Punch, which the screen counts as a sure hit. In play its four moves do this:

- Stealth Rock, 125 to 149 times a six, the most-used of the four.
- Focus Punch, 65 to 109 uses, of which 17 to 31 took HP.
- Sucker Punch, 9 to 11 percent on Bastiodon, and Explosion only 33 to 39.
- Every one of the four gets no damage comparison, so the Baton Pass flag lifts them alike.

Sudowoodo has no attack that the AI compares, and no Rock move at all.

### The picks

Each pick keeps the other five members and Ian's flags, and was run through the screen, the replacement trace and the probe on the same three boxes. Every move is legal at 52.

| Set | Knocked out while in | Wins of 150, by box | Its answers in the top sixes, and who they draw |
|---|---|---|---|
| Ian's: Sudowoodo, BrightPowder, Gentle, Sturdy; Stealth Rock, Explosion, Sucker Punch, Focus Punch | 18 to 49 | 123, 101; 84, 108; 101, 103 | Togetic, Corviknight, Gliscor, Leavanny; Corviknight and Gliscor draw a Girafarig that loses |
| 1. Magcargo, BrightPowder, Calm, Solid Rock; Shell Smash, Lava Plume, Earth Power, Ancient Power | 151 to 196 | 89, 79; 87, 110; 81, 97 | Jellicent, Manaphy, Hippowdon, Wailord (+3.0 each); nearly all draw a Sceptile that beats them |
| 2. Sudowoodo as Ian's, Earthquake for Focus Punch | 66 to 98 | 117, 118; 99, 109; 121 | not traced |
| 3. Sudowoodo, Mighty Cleave and Earthquake for Sucker Punch and Focus Punch | 70 to 100 | 111, 109; 122, 120; 121, 116 | not traced |

Magcargo is my pick because it passes Ian's bait test with a setup move, and is the only pick that makes the fight harder. The replacement rule sends it in after any member leaves against the Steel walls (Bastiodon, Bronzong, Probopass, Corviknight), which its Fire and Ground moves beat, and Earth Power hits Bastiodon four times over. Its answers are the Water and Ground types, and almost all of them draw Sceptile, which beats them. It used Shell Smash 64 to 123 times a six, the player having to answer a +2 sweeper. Solid Rock softens the super-effective hits it takes. It keeps Ian's BrightPowder and is a rarely used Pokemon with a set Kaizo would build. Shell Smash is its level 48 move, Lava Plume its 40, Ancient Power its 26, and Earth Power its tutor move. Calm is a nature no other member has.

Picks 2 and 3 keep Ian's member and give it attacks the AI compares. Its knockouts triple, but the fight reads easier. Sudowoodo then explodes far less (15 to 64 picks a six, against 68 to 90 for Ian's), and the screen finds a slightly better six for the player (22.30 against 21.70 on box 1). I list them for a Sudowoodo kept by choice.

## Part 3: the cheap checks

### The matchup screen

Bastiodon is in all 20 of the screen's top sixes on every box, and is the core of the player's answer: Weezing's Sludge Bomb cannot touch it, and only Focus Punch, Girafarig's Earthquake (75 to 90 percent) and Chatot's Heat Wave (50 to 58 percent) hurt it. Beside it the top sixes take Togetic (9 to 16 of 20), Corviknight (13 and 19 of 20 on boxes 1 and 3), Bronzong (12 to 16 on boxes 2 and 3), Gliscor (14 on box 2) and Leavanny. The screen's best score is 21.20 to 21.85 by box, higher than Saturn's 17.80 to 19.10 and Byron's 18.15 to 19.75: the player's best six answers Hesperid better than either.

The lead test, on every box: Weezing's main answer is Bastiodon (+3.0 on it, 20 of 20), which draws Sudowoodo, which beats it narrowly by Focus Punch. Corviknight draws a Girafarig that loses to it. Bronzong draws Chatot, which beats it. Weezing passes by the screen, though in play Focus Punch is the weak link.

### Speed against the box

Hesperid's Speeds in battle, against the box's likely answers at 53:

| Hesperid | Speed | Box answers it outspeeds | Box answers that outspeed it |
|---|---|---|---|
| Sceptile | 157, and 314 with Unburden on | all in the top sixes | none in the top sixes (Crobat at 150 is slower) |
| Chatot | 138 | all but Crobat | Crobat 150 |
| Girafarig | 119, and 238 after Agility | Ninetales-Alola 118, Gliscor 113, Leavanny 110, Rotom 109 | Crobat 150, Gengar 129, Staraptor 124 |
| Weezing | 73 | Bastiodon 44, Bronzong 47, Togetic 55, Probopass 55 | Corviknight 83, Altaria 97, Leavanny 110 |
| Wigglytuff | 60 | Bastiodon, Bronzong, Togetic, Probopass, Vikavolt | Corviknight, Leavanny, Gliscor, Rotom and every faster catch |
| Sudowoodo | 52 | Bastiodon 44, Bronzong 47, Garganacl and Palossand at 50 | Togetic, Probopass and everything faster |
| Magcargo (pick 1) | 52, and 104 after Shell Smash | as Sudowoodo, then Corviknight, Altaria and the slower half of the box | as Sudowoodo until it smashes |

The goal 3 reference set at 53 (Crobat 150, Talonflame 146, Weavile 145, Greninja 142, Mienshao 124, Staraptor 124, Garchomp 121, Lucario 108) gives the same picture: Sceptile outspeeds all eight, Chatot all but the four fastest, Girafarig only Lucario until it uses Agility.

### What each member does (the AI-picks probe)

Picks per 150 fights a six, over the two sixes on each of three boxes:

| Member | What the AI picks most |
|---|---|
| Weezing | Explosion on turn 1 (80 to 97 fights), then Thunder and Sludge Bomb |
| Sceptile | Leaf Storm most, then Pursuit or Rock Slide by box (Pursuit leads on box 2's most-taken six), Aerial Ace least |
| Girafarig | Earthquake and Thunder, by target; Agility 93 to 115; Baton Pass 31 to 73, after the Starf Berry |
| Sudowoodo | Stealth Rock, then Focus Punch, then Explosion and Sucker Punch |
| Wigglytuff | Hyper Beam, 186 to 332 picks a six; Perish Song 38 to 87, Calm Mind 20 to 83, Misty Explosion 2 to 32 |
| Chatot | locked by the Specs into its first pick: Heat Wave on boxes 2 and 3, a spread on box 1 |

## The egg-list commit

Commit fffae2913fb puts Explosion and Focus Punch on Bonsly's egg list and Misty Explosion on Igglybuff's, under Ian's ruling of 2026-10-29, through `learnrewrite.IAN_EGG_MOVES` and the two species files. No level-up entry moved, and the player never reaches an egg list. The draft itself is commit 28609213ad7, saved through `trainers.save` and equal to the snapshot.

## How the numbers were made

Every number comes from the worktree `.claude/worktrees/hesperid-check` on this branch. The scripts are the Candice pass's, copied to `/home/ian/.claude/jobs/382760ce/tmp/hesperid/` and pointed at this worktree; none writes to `res/`. `bc.py` is the harness: `CAND` swaps a pick into the party in memory (the sets are in its `CANDS`), and `AIBITS` with `AISTEMS` swaps the trainer's flags. It also carries the Scrappy guard described in the summary, which changes nothing unless the simulator raises that one error. `checks.py FIGHT PLACE SEED` runs the screen, the replacement trace, damage both ways and the probe: 150 rough fights against the screen's best and its most-taken six. For this check it also counts each trade move by the user's HP and by the battle's turn, each Baton Pass with the stages it passed, Sceptile's attacks with and without its item, the moves made under a Choice item, and the player's accuracy checks on a BrightPowder holder. `bait.py` is Ian's lead test, and `summarise.py` gathers the wins and knockouts. `runall.sh`, `runcands.sh`, `runcombo.sh` and `runwh.sh` ran the jobs under `tools/oxide/capped`. The first run, under the cap, is where boxes 2 and 3 crashed. One rerun of those two boxes with the guard ran without the cap, by my mistake; the same jobs then ran again under the cap and gave the same numbers. The boxes come from `plgoal3.setup` with the fresh run name `hesperid-check-study`, seeds 1 to 3, at 53 for Hesperid, Saturn 1 and Byron. Damage is the calculator's lowest to highest roll in percent of the target's HP. Legality comes from the OxiDex's `learnsets.lists` and the Kaizo checker (`oxide.py check`, with `OXIDE_OLD_RES` set to the export of 5c62989651's `res/`).

The White Herb pick (decision 4): with the herb, Sceptile attacked with Unburden on 174 to 240 times a six, where the Yache gave none, and knocked out 116 to 141 where it had 105 to 131. The fight read 116, 97; 79, 107; 92, 108, inside the probe's spread of the draft's numbers.

Where the screen's bias bites: it counts only a clean one-on-one from full HP with no status move and no hazard, and it counts Focus Punch as a sure hit, which is why it rates Sudowoodo against Bastiodon better than play does. The probe's greedy player never switches, so Pursuit never doubles, a Perish Song count always runs out on the player's Pokemon while the AI's Wigglytuff may switch away from its own, and Stealth Rock bites only after a knockout.

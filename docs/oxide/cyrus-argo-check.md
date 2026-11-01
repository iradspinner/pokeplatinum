# Argo 1 and Cyrus 1: a short check

Ian asked on 2026-10-31 to see the drafts of Officer Argo 1 (Celestic Town, a mini-boss) and Cyrus 1 (the Celestic ruins, a boss), drafted on 2026-10-13 and never put to him. They are on branch `overseer-cyrus-argo`, cut from `oxide` at 6387623469, at the levels of Cyrus 1's honour cap of 47, and the OxiDex shows them from that branch. This page checks two things only, as Maylene's did: anything that invalidates either fight, and the weakest crux of each with its top replacement picks. Nothing here is landed.

## Summary

**Outcome.** Nothing in either team breaks its fight. Every move is legal at the new levels once six moves went on egg lists. Every ability and item is modelled by the simulator and present in the engine (the engine side was checked in the code and the item data only; nothing was tried in game). No item or nature repeats within a team. The trouble is Cyrus 1's difficulty: on the cheap checks it reads far harder than any accepted fight before it. Against the same rough player that wins 42 percent of Wake's fights and 41 percent of Barry 4's, Cyrus 1 is won in 6 percent and Argo 1 in 59. The faints come from Porygon-Z and Electivire, not from Salamence.

**The two sets Ian flagged.** Neither sweeps a whole six often on these checks. Argo's White Herb Shell Smash Polteageist took all six of the player's Pokemon in 3 fights of 900, and swept everything left from three or more in 143 (16 percent). Wake's Floatzel, on Ian's own Wake team, does that in 133 of 900, so Polteageist sweeps about as often. Cyrus's Intimidate, Yache Berry and Dragon Dance Salamence took all six in none of 900, and swept the rest from three or more in 73 (8 percent), mostly from exactly three, as a closer. Cyrus's Porygon-Z swept the rest in 139 and Electivire in 64.

**The weakest cruxes.** In Argo 1 it is Aerodactyl's Taunt. The fight's fastest member, which outspeeds every catch in every box, picks Taunt on more than half its turns, so it knocks out the fewest of the player's Pokemon after the hazard lead. In Cyrus 1 it is Crobat's lead: it knocks out the fewest, its Poison and Flying moves are walled by the Rock and Steel catches the box always takes, and Taunt takes a third of its turns. Crobat passes half of Ian's lead test: every answer to it draws in a member that beats that answer (Electivire against the Rock types, Magmortar against Corviknight and Bronzong), but neither carries setup. Argo's Claydol lead passes less well: four of its seven answers draw in a member that loses to them.

**What Ian decides.**

1. Argo 1's ace level: keep Polteageist at 44, three under the cap of 47, or move the team to 43 or 45?
2. Aerodactyl's slot: my pick is Ice Fang in place of Taunt, which nearly doubles its knockouts and costs the rough player about a tenth of its wins. Or keep Taunt?
3. Argo's Claydol lead: keep it, or give it Explosion for Extrasensory, with the Check HP flag, which almost doubles its output?
4. Cyrus 1 reads far harder than Wake: soften it, have the scorer spot-check it first (two and a half to four hours), or keep it as the game's hardest fight so far?
5. Crobat's slot: keep Crobat (my pick), or take Weavile (weaker still) or Gyarados (much stronger)?
6. Honchkrow's Moxie, question 9 of the drafts' recheck: keep Super Luck, or take Moxie?
7. Polteageist's White Herb Shell Smash: keep it, on the numbers above?
8. Salamence's Intimidate, Yache Berry and Dragon Dance: keep it, on the numbers above?

**Next steps.** Ian answers in a line each. A session then applies the answers on this branch and reruns the legality check and the outcome probe, about an hour. The Overseer adds Cyrus 1's honour cap to `fights.json` before landing, since the gate's boss-level check still expects Cyrus 1 at Byron's cap of 53. A spot-check reading happens only if Ian names one.

## Part 1: what could invalidate either fight

### The teams as set

The sets are the drafts' own (745ebf383, with efb733b1d's Crunch for Honchkrow). Three kinds of change were made, and only these.

| Change | Argo 1 | Cyrus 1 |
|---|---|---|
| Levels | Polteageist 44, Claydol 43, Bronzong and Aerodactyl 42, Cofagrigus and Relicanth 41 (drafted 48 to 50) | Salamence 47, Honchkrow 46, Crobat and Porygon-Z 45, Electivire and Magmortar 44 (drafted 51 to 53) |
| AI flags | Risky dropped; Basic, Evaluate Attack, Expert and Prioritize Extremes kept | unchanged: Basic, Evaluate Attack and Expert |
| Egg lists | Baltoy takes Extrasensory, Yamask Pain Split, Relicanth Head Smash, Sinistea Shell Smash | Murkrow takes Crunch and Brave Bird |

Both teams take Mars 1's shape: the ace at the top, one member right below it, the rest two or three below the ace. Argo's ace sits three under the cap, the middle of the two to four the brief allowed, which question 1 puts to Ian.

The flags were chosen from what each team does (Ian, 2026-10-31, and the flags guide on `overseer-byron-trainers`). Argo has no critical-hit idea, so Risky was only pushing Gyro Ball, Payback, Stone Edge and Yawn at random. Prioritize Extremes stays for his Stealth Rock lead, Reflect, Will-O-Wisp, Haze, Pain Split and Shell Smash. Without it the team plays almost the same: Claydol picks Stealth Rock 123 to 148 times a run instead of 139 to 150, and the rough player wins 566 of 900 instead of 535. Cyrus's team is plain power, with no trade move, weather move, status idea or critical-hit idea for another flag to serve.

### Legality

Six moves were off-list at the new levels, and each went on its line's first-stage egg list by Ian's rule of 2026-10-29. Four of them are on no Oxide list for these lines at any level.

| Member | Move | Where Oxide has it | First stage that takes it |
|---|---|---|---|
| Claydol 43 | Extrasensory | nowhere | Baltoy, which had no egg list |
| Cofagrigus 41 | Pain Split | nowhere | Yamask |
| Relicanth 41 | Head Smash | its level 78 | Relicanth |
| Polteageist 44 | Shell Smash | its level 60 | Sinistea |
| Honchkrow 46 | Crunch | nowhere | Murkrow |
| Honchkrow 46 | Brave Bird | nowhere | Murkrow |

After the edits the OxiDex's lists give every move of both teams at its level, and the Kaizo study's checker, with the TMs from before the TM pass, finds one note only: Salamence at 47 sits three under Shelgon's 50. The rulings allow a member under its evolution level when it is not egregiously early. One side effect: with an egg list, the learnset generator would move Baltoy's and Claydol's level 1 Self-Destruct and Explosion onto it if Baltoy were ever rewritten. The files are the authority, so this is only a note in `test_learnrewrite`.

### The rest of the rulings

These pass, and none needs a decision.

- Items: none repeats. Each is modelled in the simulator, the type boosters through its booster table, and each is a Generation 4 hold effect the engine has. In the probe, Polteageist's White Herb went in 55 to 141 fights of 150, about once for each Shell Smash; Salamence's Yache Berry went in 16 fights on one box only, since few catches carry Ice moves.
- Natures: none repeats.
- Abilities: Mummy, Cursed Body and Unnerve run in the simulator since 2026-10-14 and are in the engine. Download raises one stat a stage on entry. Intimidate counts once.
- Banned moves: no one-hit KO move, no evasion move and no trapping move. Neither team carries a forced trade.
- Luck items: Crobat's Razor Fang is allowed (Ian, 2026-10-06), and so is Aerodactyl's Wide Lens.

### Speed at the box's 47

| Member | Speed | Outspeeds (box 1, 2, 3) |
|---|---|---|
| Aerodactyl | 139 | every catch |
| Claydol | 87 | 55 of 91, 50 of 93, 66 of 88 |
| Polteageist | 80, or 160 after Shell Smash | 51, 50 and 61; after Shell Smash every catch |
| Relicanth | 62 | 27, 28 and 34 |
| Bronzong and Cofagrigus | 40 and 42 | 5 or fewer |
| Crobat | 148 | every catch |
| Electivire | 122 | 86, 86 and 85 |
| Salamence | 113, or 169 after Dragon Dance | 84, 80 and 85; after Dragon Dance every catch |
| Magmortar | 110 | 82, 77 and 85 |
| Honchkrow | 102 | 78, 72 and 81 |
| Porygon-Z | 99 | 69, 70 and 78 |

Every member of Cyrus 1 outspeeds three catches in four or more. The boxes' fastest catch is 134.

## Part 2: how each fight plays, and its weakest crux

Both fights were read on goal 3's three boxes at Cyrus 1's stretch, the box at 47 for both. Argo has no cap of his own, so the player may meet him at 47; goal 3's own rule would put the box at his ace's 44. Each run is 150 rough fights against one six, the screen's best ("answers") and its most common, so six runs a fight. Their win numbers mean little alone, and so Wake and Barry 4 were run the same way to give them a scale.

| Fight | The rough player's wins, of 150, by run | All runs |
|---|---|---|
| Argo 1 | 118, 121, 66, 79, 77, 74 | 535 of 900 |
| Wake | 95, 67, 28, 66, 55, 67 | 378 of 900 |
| Barry 4 | 52, 80, 71, 45, 59 | 307 of 750 |
| Cyrus 1 | 15, 8, 22, 5, 1, 1 | 52 of 900 |

The matchup screen agrees in direction. Its best six scores about 21 against Argo and 13 to 14 against Cyrus, and against Cyrus most catches lose the one-on-one to most of his members.

### Who knocks out the player's Pokemon

The player's Pokemon knocked out while each member was in, the lowest and highest of the six runs:

| Argo 1 | Claydol | Bronzong | Cofagrigus | Relicanth | Aerodactyl | Polteageist |
|---|---|---|---|---|---|---|
| Knocked out while in | 9 to 46 | 68 to 161 | 83 to 131 | 87 to 143 | 65 to 90 | 192 to 314 |

| Cyrus 1 | Crobat | Honchkrow | Porygon-Z | Electivire | Magmortar | Salamence |
|---|---|---|---|---|---|---|
| Knocked out while in | 28 to 117 | 74 to 162 | 128 to 331 | 138 to 269 | 98 to 136 | 97 to 198 |

### The two sets Ian flagged

A sweep is counted per fight. "All six" means the one member knocked out all six of the player's Pokemon. "Swept the rest" means it took the player's last Pokemon and every one still standing when it first came in, three or more.

| Member | All six | Four or more | Swept the rest | Setup used, per run of 150 | Its knockouts made while raised |
|---|---|---|---|---|---|
| Polteageist (Argo) | 3 of 900 | 97 | 143 | Shell Smash 54 to 141 | 49 of 194 to 193 of 298 |
| Salamence (Cyrus) | 0 of 900 | 12 | 73 | Dragon Dance 17 to 46 | 27 of 99 to 65 of 198 |
| Porygon-Z (Cyrus) | 2 of 900 | 68 | 139 | none (Download raises it on entry) | nearly all |
| Electivire (Cyrus) | 1 of 900 | 57 | 64 | none | none |
| Floatzel (Wake) | 0 of 900 | 50 | 133 | | |

Polteageist sweeps far more on two boxes than the third: box 1 gives it 22 sweeps of the rest, boxes 2 and 3 give it 68 and 53. Salamence uses Dragon Dance in 17 to 46 fights of 150. The AI rates Earthquake and Dragon Claw above it, so most of its sweeps are of the last three Pokemon at the fight's end. Salamence is not what makes Cyrus 1 hard.

### Argo's lead, by Ian's test

Claydol sets Stealth Rock on its first turn in 133 to 140 fights of 150, and makes the fewest knockouts. Its answers, and who the trainer AI's replacement rule sends in when it leaves:

| Claydol's answer (its margin on Claydol) | Drawn in | Who wins that one-on-one |
|---|---|---|
| Corviknight (+2.5), in all 20 of the top sixes on boxes 1 and 3 | Relicanth | Relicanth (-1.5) |
| Ninetales-Alola (+2.5) | Bronzong | Bronzong (-2.5) |
| Abomasnow (+2.5) | Aerodactyl | Aerodactyl (-0.5) |
| Bronzong (+3.0) | Cofagrigus | the player's Bronzong (+3.0) |
| Orbeetle (+3.0) | Cofagrigus | Orbeetle (+0.5) |
| Milotic (+3.0) | Bronzong | Milotic (+1.5) |
| Jynx (+2.5) | Cofagrigus | Jynx (+1.5) |

So four answers of seven draw in a member that loses to them, and none draws in Polteageist, the setup member. Polteageist is drawn in when Aerodactyl's Water and Ground answers stay in: Quagsire, Whiscash and Crawdaunt draw it in and lose to it, and Kingler draws it in and beats it (+0.5). Aerodactyl's other answers, Donphan, Hippowdon and Milotic, draw in Relicanth and beat it (+0.5). So Aerodactyl meets Ian's test against about half its answers, the half that draws in the Shell Smash user.

### Argo's crux: Aerodactyl's Taunt

Aerodactyl outspeeds every catch in every box, yet makes the fewest knockouts after the lead. It picks Taunt 170 to 329 times a run, more than its three attacks together. Expert drives most of that. On the base flags alone it still picks Taunt 69 to 175 times, so dropping Prioritize Extremes does not fix it. Taunt does little against a box that mostly attacks.

| Set | Legal | Aerodactyl's knockouts, per run | The rough player's wins |
|---|---|---|---|
| Drafted: Stone Edge, Earthquake, Fire Fang, Taunt | yes | 65 to 90 (77 on average) | 535 of 900 |
| 1. Ice Fang for Taunt | yes (a level 1 move) | 109 to 161 (134 on average) | 403 of 750, five runs |
| 2. As drafted, the base flags alone | yes | 59 to 112 | 566 of 900 |

Ice Fang is my pick. It hits Torterra four times over and Donphan, Hippowdon and Tsareena twice. With it, the AI spreads its picks across all four attacks, and the rough player wins 81 fights a run on average instead of 89. The Taunt set stays the gentler choice.

Claydol has a pick of its own, question 3. With Explosion in place of Extrasensory and the Check HP flag (the flags guide's rule for an exploder), Claydol's knockouts rise from 193 to 287 over the six runs, and it explodes 19 to 42 times a run. The rough player wins 515 of 900 against 535. Shadow Ball in place of Extrasensory was also tried, against its Psychic answers. The AI seldom picks it, so that set reads the same as the draft.

### Cyrus's lead, by Ian's test

Crobat's answers are the Rock and Steel catches: Bastiodon (+3.0, in 17 to 20 of the top 20 sixes on every box), Probopass (+3.0), Golem (+3.0), Garganacl (+3.0), Glimmora (+2.5), Rhydon (+2.5) and Corviknight (+2.5). The Rock answers draw in Electivire, whose Brick Break beats Bastiodon (-1.5), Probopass (-2.5), Garganacl (-1.5) and Glimmora (-1.5). Golem and Rhydon narrowly beat Electivire (+0.5), and then Electivire's leaving draws in Salamence, which beats them both. Corviknight and Bronzong draw in Magmortar, which beats them (-1.5). So the lead passes the drawn-member half of Ian's test against every answer, as Maylene's Pawmot did, but the member drawn in has no setup move.

### Cyrus's crux: Crobat's slot

Crobat makes the fewest knockouts of the six, 28 to 117 a run. Brave Bird and Cross Poison are resisted by the Rock and Steel catches the box always takes. Its Taunt takes about a third of its turns, and Crobat has nothing in its palette that hits Steel well.

| Set in the lead slot, at 45 | Legal | Its knockouts, per run | The rough player's wins |
|---|---|---|---|
| Drafted Crobat: Razor Fang, Jolly; Cross Poison, Brave Bird, U-turn, Taunt | yes | 28 to 117 | 52 of 900 |
| Weavile: Razor Fang, Jolly; Knock Off, Ice Punch, Brick Break, Poison Jab | yes | 29 to 72 | 59 of 900 |
| Gyarados: Wacan Berry, Jolly, Intimidate; Waterfall, Earthquake, Ice Fang, Thunder Wave | yes | 144 to 271 | 8 of 900 |

My pick is to keep Crobat. Weavile's Brick Break answers Bastiodon, but it is frailer, makes fewer knockouts than Crobat, and its Fighting answers draw in Honchkrow, which beats them without setup. Gyarados makes more knockouts in its worst run than Crobat in its best, and it would make the hardest fight in the game so far nearly unwinnable for the rough player. Both are canon picks Cyrus could keep for his later fights.

### Cyrus 1's difficulty

Cyrus 1 was drafted on 2026-10-13 for Byron's cap of 53, against a box with all of Byron's split to draw on. At the cap of 47 it meets a box cut at Celestic Town, and its six fully evolved members outspeed most of it. Question 4 asks Ian what he wants. One cheap dial was tried: Porygon-Z with its hidden Analytic in place of Download. Its knockouts fall from 1401 to 1051 over the six runs, and the rough player's wins rise from 52 to 75 of 900, still far below Wake's 378. A real softening would need more than one dial, and the scorer's spot check is the measure Ian uses when a fight looks clearly off (2026-10-22).

## How the numbers were made

Every number comes from a run in the worktree `.claude/worktrees/cyrus-argo` at 4f3582ea14. The scripts are in `/home/ian/.claude/jobs/cyrus-argo/`, each with its own usage line, and none writes to `res/`. They are Maylene's scripts, made to take a fight and to swap a candidate in memory.

- `common.py` builds a fight on goal 3's box for a seed, with the box at 47 (`plgoal3.setup` and `fight_state`, the level overridden), and runs the matchup screen.
- `margins.py` prints the screen's catches, their moves, Speeds and margins on each member.
- `replace.py` runs the trainer AI's own replacement rule (`fightai.replacement`) for each member leaving, against each catch the top 20 sixes take twice or more.
- `outcome.py` is the AI-picks probe and the outcome probe in one: 150 rough fights per six, a greedy player (85 percent of turns its hardest hit by the lowest roll, otherwise a random action, the simulator's own pick after a knockout). It counts each member's picks and uses, items spent, knockouts, and the sweeps above. It counts nothing the player's replacement look-ahead tries.
- `speed.py` gives the Speed tiers; `legal.py` the legality, from the OxiDex's `learnsets.lists` and the Kaizo study's checker with `OXIDE_OLD_RES` at an export of 5c62989651's `res/`.
- `cand.py NAME SCRIPT SEED` swaps one candidate into its slot (`common.swap`), with `AIBITS` setting the trainer's flags for a run.

Where the probe's bias bites: the greedy player never switches against a setup move and never uses a status move, so every sweep number above runs high against a careful player, and the more so for Shell Smash and Dragon Dance. The screen counts a clean one-on-one from full HP with no status, so it never sees Taunt, Yawn, Will-O-Wisp, Stealth Rock or Reflect. Wake and Barry 4 were read with goal 3's own box level, at their caps.

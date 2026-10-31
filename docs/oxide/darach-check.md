# Darach and Caitlin's six: a short check

Ian built a first draft of Darach and Caitlin, the Castle Valet, on 2026-10-31: an optional boss in Wake's split (cap 44), fought in the Pokemon Mansion's entrance hall on Route 212 North. It gates the mansion, the maids' knockout and the Trophy Garden, and the Manaphy egg comes on the win. The fight is a double battle as one trainer, with no field rule. He asked for three things: anything that invalidates the fight, the weakest crux with the top replacement picks for it, and how it reads against Dahlia and Wake. The six is in a spare slot (`dummy_008`) on branch `overseer-darach`, for study only. No reading reads a double battle yet, so every number below is a proxy, and the doc says which kind each one is.

## Summary

**Outcome.** Nothing breaks the fight. Every ability, item and move works in Oxide's engine in a double, and the trainer AI plays most of the six well: Corviknight raises Tailwind on the first turn in about nine fights of ten, and Entei uses Bulldoze almost only beside a partner it cannot hurt. Ten moves across all six members were on no list at 44, and each is now on its line's first stage's egg list, by Ian's ruling of 2026-10-29 (Part 1). The one real flaw is Galarian Rapidash's Heal Pulse. The AI never aims it at its partner, so it aims it at one of the player's Pokemon, nearly always one at full HP, where it fails. It picks it 177 to 291 times in the first two turns of 300 fights, and now and then it heals a hurt Pokemon of the player's. As a double on the simulator it reads as hard as Wake's six would as a double on box 1, and harder on boxes 2 and 3. Played one at a time, as a single battle, it is easier than Wake on boxes 2 and 3, so the double itself carries the difficulty. Together that puts it at about Wake's level or a little above.

**The weakest crux is Galarian Rapidash's slot.** It knocks out the fewest of the player's Pokemon on two boxes of three, spends its first turn on a Heal Pulse that fails, and is the third Fire type. The three Fire types share the boxes' main answer, Earthquake. Hippowdon is in nearly every top six on boxes 2 and 3, and the stand-in player's best lead pairs lean on it. Changing the slot moved the proxy little: Swords Dance for Heal Pulse read the same, and Incineroar read harder on one box and easier on another.

**What Ian decides.**

1. Where should the fight sit: at about Wake's level, where it reads now, or Dahlia's shape (too hard in its own split, fair in Byron's)?
2. Rapidash's slot. My first pick is his Rapidash with Swords Dance for Heal Pulse; my second is Incineroar. Or keep Heal Pulse and approve an AI change that aims it at a hurt partner. The sets are in Part 3.
3. The Focus Sash is on a lead that carries no forced trade. The ruling of 2026-10-06 names only a trade lead. Is it fine here?
4. Entei's Ability Shield guards Pressure, which does next to nothing, so the item is close to empty. Keep it, or choose another?
5. Tailwind lasts three turns counting the turn it goes up, as in Generation 4, so it speeds Darach's side for two turns; the later games give four. Keep Generation 4's count?

**Next steps.** Ian answers in a line each. A session then applies the chosen set on this branch and reruns the legality check and the proxies below, which takes about an hour. A check against Byron's boxes, if he wants Dahlia's shape, is about an hour more. An AI change for Heal Pulse, if approved, is about two hours with its test and the simulator's mirror. The fight's placement (the gate script, the egg's handover and its capture in the OxiDex) is the later job in the tracker's Frontier Brains entry. A real reading of the fight waits on the doubles planner, which is not built.

## Part 1: what could invalidate the fight

### Legality

Ten moves across all six members were on no Oxide list at 44, by the OxiDex's lists and by the Kaizo checker with the pre-TM-pass TMs. Each now sits on the egg list of its line's first stage, by Ian's ruling of 2026-10-29, in commit 10844608823 on this branch. No level-up entry moved.

| Member | Move | Where Oxide had it | Egg list it went on |
|---|---|---|---|
| Galarian Rapidash | High Horsepower | nowhere | Ponyta (its first stage, by the Moon Stone) |
| Corviknight | Roost | Corviknight's level 65 | Rookidee |
| Corviknight | Tailwind | nowhere | Rookidee |
| Sinistcha | Protect | nowhere | Sinistea (by the Leaf Stone) |
| Armarouge | Scorching Sands | nowhere | Charcadet |
| Galarian Articuno | Freezing Glare | its own level 45 | its own |
| Entei | Sacred Fire, Crunch, Extreme Speed, Bulldoze | nowhere | its own, a new list |

Protect left every list the player can use on 2026-10-06; an egg list is the trainers' palette only, so the player still has none. Entei's data had no egg list, so it now has one. Each entry is in the generator's list of Ian's egg moves too, and none of these lines is held out. After the edits both checkers pass all 24 moves at 44, the trainer lint finds nothing, test_learnrewrite passes 5 of 5 and test_learncheck 18 of 18.

### What each piece does in Oxide's engine, in a double

I read the engine and the battle scripts for each piece; the simulator's own double battle models each of them too.

| Piece | What it does here |
|---|---|
| Hospitality (Sinistcha) | As it comes in during a double, a hurt partner gets back a quarter of its HP. At the battle's start the partner is at full HP, so it acts only on a later switch-in |
| Pastel Veil (Galarian Rapidash) | Blocks poison on itself and its partner, and cures a poisoned partner as it comes in |
| Mirror Armor (Corviknight) | Turns any stat drop from the other side back on its user, Intimidate included |
| Competitive (Galarian Articuno) | Two stages of Sp. Atk for each stat a foe lowers, Intimidate included; its partner's moves do not set it off |
| Flash Fire (Armarouge) | Absorbs a Fire move from either side, its partner's too, and powers up its own Fire moves by half |
| Heal Pulse | Can be aimed at the partner in a double; heals half the target's HP; fails at full HP, on a Substitute and under Heal Block |
| Tailwind | Doubles the Speed of both of Darach's Pokemon. It lasts three turns counting the turn it goes up, so it speeds the order of the next two turns; it has 1 PP, so it goes up once a fight |
| Incinerate | Hits both foes at 60 power, each hit at three quarters while both stand, and burns up a Berry |
| Bulldoze | Hits every other Pokemon, its partner too, at 60 power, three quarters each, and lowers Speed. Corviknight and Galarian Articuno are immune; Rapidash, Armarouge and Entei's other partners are hit, and the three Fire types take double |
| Matcha Gotcha | Hits both foes at 80 power, three quarters each, 90 percent accuracy; drains half the damage of each hit, plus three tenths with Big Root; burns 20 percent |
| Strength Sap | Heals by the target's Attack, its stage included, plus three tenths with Big Root, then lowers that Attack; fails at -6 |
| Freezing Glare | 90 power, raised a fifth by the Mind Plate, with a 10 percent freeze |
| Sacred Fire | 100 power, 95 percent, a 50 percent burn |
| Extreme Speed | Priority +2, 5 PP |
| Ability Shield | Does what the later games' item does: no Mold Breaker, Neutralizing Gas, Skill Swap, Worry Seed, Entrainment or Gastro Acid touches its holder's ability. Pressure is what it guards |
| Focus Sash, Assault Vest, Leftovers, Mind Plate, Big Root | Work as usual; the Vest raises Armarouge's Sp. Def by half |

### The trainer AI in a double

In a double Oxide's engine forces Tag Strategy on for every trainer, so Ian's flags behave as if `AI_FLAG_TAG_STRATEGY` were set. The AI scores each move against each of the other three Pokemon in turn, its partner included. It drops the partner as a target unless the partner's best move there scores 100 or more, then takes the target with the highest best score. The simulator's chooser mirrors this routine, so I played the six through the simulator's double battle against each box's best six and counted what the AI picked (900 fights a split, Part 2). What it does:

- Heal Pulse goes to a foe, always. Tag Strategy scores a status move against the partner at -30 unless it is one of the few moves the routine has a case for, and Heal Pulse is not, so the partner is never chosen. No routine scores Heal Pulse against a foe either, so it stays at the starting 100 and often ties the best attack. Rapidash used it 717 times in 900 fights, every time on one of the player's Pokemon: 641 times on one at full HP, where it failed, and 76 times it healed a hurt one.
- Tailwind is used well. Corviknight raised it in 897 fights of 900, in 781 of them on the first turn. It goes up at Corviknight's Speed of 77, so it does not change the first turn's order.
- Bulldoze is used well. Tag Strategy scores it as Earthquake: +2 beside a Flying partner, -10 beside a Fire one, -3 beside Sinistcha. Of Entei's 386 Bulldozes, all but 3 came beside Corviknight or Galarian Articuno.
- Entei lights Armarouge's Flash Fire. Tag Strategy gives a Fire move at a Flash Fire partner +3, which clears 100, so Entei aimed Sacred Fire at Armarouge 113 times. That spends Entei's turn to raise Armarouge's Fire moves, a fair trade at best.
- Protect is used often. The Expert routine gives Protect +2 in every double, so Sinistcha used it 847 times in 900 fights, though rarely twice in a row.
- Strength Sap is nearly unused, 82 times in 900 fights.

Where the AI plays these sets badly: Heal Pulse, above all, and Entei's Sacred Fire into its own partner. Everything else is sound. Nothing here changes the AI, the simulator or the scorer.

### The rulings

No item repeats and no nature repeats. No member carries a forced trade, a one-hit KO move, an evasion move or a trap. Hypnosis is a sleep move and keeps Generation 4's 60 percent, as the move rulings say sleep moves do; trainers are welcome to such moves (2026-10-06). No ruling covers freezing; Freezing Glare's 10 percent is the later games' number. The Focus Sash is the one open point. The ruling of 2026-10-06 lets a Sash go on a lead that carries the boss's trade, and Rapidash carries none, so question 3 asks Ian. In a double the Sash breaks on the first hit of any kind, spread moves included.

### Gaps found

- Goal 3's boxes for Wake's split hold Manaphy, the prize of this very fight: the roll counts the Mansion's egg as caught in the split. It is in 5 of box 1's top sixes and 2 of box 3's, so those boxes are a little flattered. That is a tooling question for the Overseer.
- Goal 3 refuses a double battle, and the doubles helper builds its side from the split, not from a box, so this study built both states itself (below).
- Tailwind's three turns are Generation 4's; the simulator counts the same (question 5).

## Part 2: the fight against the boxes

### Two proxies, since no reading reads a double

The first proxy plays Darach's six as an ordinary single battle (no partner, no Tag Strategy) with the greedy player of Dahlia's study: it never switches, never sets up and has no items. It is run beside Wake and Dahlia on the same boxes and seeds. The second plays the real double on the simulator's own double battle, with its stand-in player, which picks the attack worth the most and never switches. It is run over all 15 lead pairs of the screen's best six, 20 fights a pair. As a yardstick it is also run against Wake's six fought as if his fight were a double, which it is not. Only the comparisons in each table mean anything.

| Box | Greedy wins of 150, singles: Darach's six | Wake | Dahlia (room on) | Stand-in wins of 300, doubles: Darach | Wake's six as a double | Best lead pair's wins of 20: Darach | Wake's six as a double |
|---|---|---|---|---|---|---|---|
| Wake 1 | 15 | 16 | 110 | 42 | 36 | 11 | 8 |
| Wake 2 | 60 | 22 | 17 | 36 | 60 | 6 | 9 |
| Wake 3 | 40 | 24 | 30 | 31 | 121 | 11 | 18 |

One at a time, Darach's six is about as hard as Wake on box 1 and easier on boxes 2 and 3. As a double it is as hard as Wake's six as a double on box 1 and clearly harder on boxes 2 and 3. Put together, the fight reads at about Wake's level or a little above it. Dahlia, on the same boxes, reads as Wake on boxes 2 and 3 and far easier on box 1. The matchup screen's best six (higher is easier, damage one-on-one only) is 13.10, 12.80 and 12.80 against Darach, against Wake's 8.55, 7.35 and 7.35; the screen sees no partner, no spread move and no Tailwind, so it says little here.

### Turn one, and the pairs

Darach leads Galarian Rapidash and Corviknight, his party's first two. On turn one Corviknight raises Tailwind, which goes up after most of the player's leads have moved. Rapidash, faster than every common catch but Greninja, uses Heal Pulse on a full-HP foe in most fights, or Play Rough otherwise. So the first turn is Darach's weakest: one move fails and the other sets up. The player's best answer is to put both hits into one target. Rapidash's Sash breaks on the first and the second knocks it out; Corviknight lasts longer, with Leftovers, Roost and Mirror Armor. Then for two turns every one of Darach's six moves first.

The stand-in's best lead pairs, by box:

| Box | Best pairs (wins of 20) |
|---|---|
| Wake 1 | Probopass with Kingler 11, Probopass with Golem 11, Corviknight with Probopass 6 |
| Wake 2 | Rotom with Hippowdon 6, Staraptor with Hippowdon 6, Golem with Hippowdon 5 |
| Wake 3 | Corviknight with Hippowdon 11, Corviknight with Golem 5, Corviknight with Gothitelle 4 |

Hippowdon and the Rock types are the answer. An Earthquake hits Rapidash, Armarouge and Entei for double, and Darach's side has three Fire types, while only Corviknight and Galarian Articuno are immune. Probopass resists Brave Bird, Play Rough and Galarian Articuno's Psychic, though Rapidash's High Horsepower hits it four times over. Every pair led by Luxray lost all 20 on box 1, though Luxray is the screen's top pick against Corviknight.

Darach's strongest pairs, by hand. Corviknight with Entei is the best: Entei's Bulldoze hits both foes freely beside a Flying partner, Extreme Speed picks off what is hurt, and Corviknight's Mirror Armor turns back the drops. Sinistcha with Armarouge doubles the spread damage, and Hospitality heals Armarouge as Sinistcha comes in. Galarian Articuno with either Flying partner leaves Earthquake nothing to hit but the other. The answers that break them are a spread Earthquake against any pair with two Fire types, and Electric and Rock against the two Flying types (Probopass's Discharge hits both).

### What the AI picked

Over 900 rough double battles a split (three boxes, 300 each), the moves Darach's side picked:

| Member | Picks |
|---|---|
| Galarian Rapidash | Heal Pulse 717, Play Rough 436, High Horsepower 200, Fire Lash 36 |
| Corviknight | Brave Bird 3401, Iron Head 2403, Tailwind 897, Roost 464 |
| Sinistcha | Matcha Gotcha 1409, Protect 847, Shadow Ball 437, Strength Sap 82 |
| Armarouge | Energy Ball 606, Incinerate 398, Scorching Sands 339, Psychic 85 |
| Galarian Articuno | Ancient Power 448, Freezing Glare 435, Hypnosis 410, Shadow Ball 87 |
| Entei | Sacred Fire 828 (113 at Armarouge), Extreme Speed 531, Bulldoze 386, Crunch 221 |

Corviknight's high counts come from how long it stays in. It stood in the battle for 1305 to 1677 of the player's knockouts per 300 fights, the most of the six on every box.

### Speed tiers

| Member | Speed | Under Tailwind |
|---|---|---|
| Galarian Rapidash | 115 | 230 |
| Galarian Articuno | 112 | 224 |
| Entei | 106 (and Extreme Speed at +2) | 212 |
| Armarouge | 84 | 168 |
| Sinistcha | 80 | 160 |
| Corviknight | 77 | 154 |

| The catches the top sixes take four times or more | Speed |
|---|---|
| Greninja | 118 |
| Staraptor | 104 |
| Manaphy, Ninetales-Alola | 99 |
| Luxray, Pachirisu | 95 |
| Rotom | 91 |
| Kingler | 77 |
| Corviknight | 70 |
| Gothitelle | 68 |
| Empoleon | 64 |
| Plusle, Crawdaunt | 60 |
| Hippowdon, Golem, Probopass, Quagsire | 42 to 52 |

Without Tailwind, Rapidash, Articuno and Entei outspeed every common catch but Greninja, and the rarer Crobat (126), Weavile (121), Cinderace (116), Salazzle (114) and Liepard (113). Armarouge, Sinistcha and Corviknight move after everything from Rotom up, and before the walls (Corviknight ties Kingler). Under Tailwind all six outspeed every catch the screens take. Staraptor carries Tailwind in its four on boxes 1 and 2, and with both sides' Tailwind up the order goes back to normal.

## Part 3: the weakest crux

### Why it is Galarian Rapidash's slot

Rapidash knocked out the fewest of the player's Pokemon while it stood on boxes 1 and 2 (108 and 209 per 300 fights, against 1305 to 1677 for Corviknight), and the second fewest on box 3. Three things weaken it.

1. Its Heal Pulse cannot reach its partner (Part 1), so it fails or heals the player, 717 times in 900 fights.
2. It is the third Fire type. Earthquake hits it, Armarouge and Entei for double, and Hippowdon is in 19 or 20 of the top 20 sixes on boxes 2 and 3.
3. Its Focus Sash breaks on the first hit, and the player has a free turn to put two into it while Corviknight sets Tailwind.

### The picks

Each pick keeps Ian's other five as they stand and was swapped into the lead's slot in memory. Each ran through the screen and the rough double battles over all 15 lead pairs on the same three boxes.

| Set | Legal at 44 | Stand-in wins of 300 in doubles, boxes 1, 2, 3 | Best lead pair's wins of 20 | What the AI did with it |
|---|---|---|---|---|
| Ian's: Galarian Rapidash, Focus Sash, Adamant, Pastel Veil; Heal Pulse, Fire Lash, Play Rough, High Horsepower | yes, after the egg lists | 42, 36, 31 | 11, 6, 11 | Heal Pulse at a foe 717 times in 900 |
| 1. Ian's Rapidash with Swords Dance for Heal Pulse | yes (Ponyta's egg list has it since Dahlia) | 43, 23, 38 | 13, 6, 12 | Swords Dance 452 times; knockouts while it stood rose to 151, 231 and 309 |
| 2. Incineroar, Shuca Berry, Impish, Intimidate; Fake Out, Parting Shot, Darkest Lariat, Blaze Kick | yes, every move | 26, 56, 36 | 6, 7, 5 | Parting Shot 1106 times, cycling Intimidate in; Fake Out only 151 |
| Tried and set aside: Hitmontop, Sitrus Berry, Adamant, Technician; Fake Out, Triple Kick, Mach Punch, Sucker Punch | yes, every move | 21, 116, 57 | 6, 17, 13 | Fake Out only 130 times |
| Tried and set aside: Clefable, Rocky Helmet, Calm, Magic Guard; Follow Me, Moonblast, Icy Wind, Moonlight | yes, every move | 40, 80, 80 | 9, 12, 14 | Follow Me 797 times |

With 300 fights a box, a gap of about six wins is noise.

Pick 1 is my first choice, because it is the smallest change that fixes the flaw. It keeps Ian's member, item, nature and ability, and changes one move. The fight reads the same by the proxy, but the AI stops healing the player's Pokemon, which a player would see as the AI playing badly. With its Sash, a Swords Dance on the first turn is safe, and under Tailwind a +2 Rapidash moves first for two turns. A player who sees it has one turn to answer. It keeps the three Fire types and their shared Ground weakness, which is the hole the player has to find.

Pick 2 is Ian's own first plan for Darach (`frontier-brains.md`). Incineroar is the classic double partner: Intimidate on both foes as it comes in, Fake Out, and Parting Shot to switch out and bring Intimidate back. The AI plays it as a pivot, using Parting Shot more than anything else. It reads harder on box 1, easier on box 2 and the same on box 3, and it cuts the best lead pairs' wins to 5 to 7 of 20 on every box. Against these physical-heavy boxes (Hippowdon, Golem, Kingler, Staraptor, Luxray) Intimidate is worth more than it looks. The Shuca Berry halves one Earthquake. It is still a third Fire type, so the Ground hole stays.

Hitmontop and Clefable fix the Fire overlap but make the fight easier on two boxes of three. The AI rarely uses Fake Out on the first turn, since Expert gives it only +2 and the attacks often score as high. Clefable used Follow Me often, but drawing the hits onto itself made the fight easier, not harder. So I set both aside.

## How the numbers were made

Every number comes from a run in the worktree at 10844608823 (Ian's draft at 8d0f1f99130 plus the egg lists). The scratch scripts are in `/home/ian/.claude/jobs/382760ce/tmp/darach/`, each with its own usage line, and none writes to `res/`.

- The boxes come from `plgoal3 --run darach-study --box wake <seed> --screen` for seeds 1 to 3, a run name with no earlier results. They are at 44.
- `darach.py` is the harness every script loads. It adds Darach's constant to the trainers the balance tools read, since no map battles him yet. Goal 3's own fight setup refuses a double, so the harness builds two states from the simulator's own preparation with the box as the side: a single battle's, for the matchup screen, and a double's, for the simulator's double battle. `CAND=name` swaps a pick into the lead's slot in memory; `OTHER=316` plays Wake's six through the same harness, as the yardstick.
- `margins.py` prints the screen's top sixes and every taken catch's four moves, Speed and margins against the six.
- `dfights.py` plays the simulator's double battle (`run_doubles`) with the trainer side on the AI's doubles chooser and the player on the stand-in, over every lead pair of the screen's best six. It counts every pick with its target (foe, ally, both foes, self), where Heal Pulse went and whether its target was at full HP, Tailwind's turn, Bulldoze's partner, and the player's knockouts while each of Darach's six stood. A knockout is counted for both of Darach's Pokemon on the field, so those counts overlap.
- `compare.py` runs Dahlia's greedy player against Darach's six as a single battle and against Wake; `compare_dahlia.py` runs her own study's comparison on these boxes, through a copy of her harness pointed at this worktree. Her box 1 number is 110 today, against 101 in her study, from changes to the tree since.
- Legality comes from `legal.py`, which uses the OxiDex's `learnsets.lists`, and from `oxide.py check 44`, with `OXIDE_OLD_RES` set to the export of 5c62989651's `res/`. `palette.py` lists a species' legal moves at a level.

Where the proxies' biases bite. The stand-in never switches, never sets up and does not aim a move at its own partner, so its wins are far below a real player's, and it never plays around Hypnosis or Tailwind. The simulator's double battle lacks the gaps that batch 15 left open (the simulator gaps doc's double battles section): no Lightning Rod or Storm Drain draw, a screen at a third off always, a spread move's three quarters judged once for the whole move, and no switching by choice on either side, though the engine's AI may switch in a double. The single-battle proxy drops the partner, the spread moves and Tag Strategy altogether.

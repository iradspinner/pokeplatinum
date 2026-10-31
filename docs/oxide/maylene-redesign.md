# Maylene's six: a short check

Ian built Maylene's six (Veilstone Gym, Maylene's split, cap 39) in the OxiDex on 2026-10-29 and asked for two things only: anything that invalidates the fight, and the weakest crux with the top replacement picks for it. His natures are his choice and are not argued here. The six is on branch `overseer-maylene` (0d358a4505) for study only; nothing here lands.

## Ian's answers (2026-10-29)

Hakamo-o keeps his set (question 1), so Toxicroak and the Bulk Up set are not taken. Cacturne takes its hidden ability, Water Absorb (question 4). Every move his six carries that no list gives at its level goes on the egg list of its line's first stage, and he ruled that this is done from now on without asking him, never by moving a level-up entry, since that would change what the player gets (question 2). So Pawmi's list takes Sucker Punch and Volt Switch, Heracross's Close Combat and Bug Bite (Close Combat stays its level 37 move for the player, which answers question 3), Jangmo-o's Dragon Dance and Focus Punch, and Cacnea's Fling, which is legal as a TM cut in the TM pass but which the OxiDex's list reads as off-list. Question 5 falls away with Toxicroak.

## Summary

**Outcome.** Nothing breaks the fight in the simulator, and every item and every move does what Ian meant there (the engine side was checked only in the item data; nothing was tried in game): the Flame Orb burns Heracross for Guts and Facade, the Iron Ball halves Cacturne's Speed to 25 for Revenge and Payback and is then flung at 130 power (Cacturne is at 51 afterwards), and Pawmot's Volt Switch hands the field to Lucario. Two things fail as the file stands. Five moves on three members are on no Oxide list for their species before Cyrus 3's split. And Cacturne's Sand Veil does nothing, since nothing in this fight sets a sandstorm.

**The weakest crux is Hakamo-o's slot.** It knocks out the fewest of the player's Pokemon of the six in every probe run (19 to 60 per 150 fights, against 158 to 248 for Lucario). Its set is two conditional moves, a 1 PP Dragon Dance and Outrage. Under Ian's Risky and Prioritize Extremes flags the AI picks Counter most and Outrage least. Every Fairy in the boxes knocks it out from full HP in one hit, and the AI's replacement rule almost never sends it in, so the team's only setup move rarely gets used. Pawmot's lead passes Ian's bait test: every answer to it draws in Lucario or Medicham, which beat that answer.

**What Ian decides.**

1. Hakamo-o's slot: my first pick is Toxicroak with Swords Dance; my second is Hakamo-o with Bulk Up in place of Counter and Dragon Dance, fully legal; my third is Hakamo-o keeping Dragon Dance. Or keep his set. The sets and their numbers are below.
2. Make Pawmot's Sucker Punch and Volt Switch and Heracross's Bug Bite legal through the egg lists, as he did for Fantina, or swap them for legal moves? Dragon Dance and Focus Punch need the same call only if Hakamo-o keeps them.
3. Heracross's Close Combat is its level 37 move, one level past its 36 and inside Maylene's split. Is that covered by his ruling of 2026-10-13 (a level-up move learned just after the split), or should Heracross go to 37?
4. Cacturne: keep Sand Veil, which does nothing here, or take its hidden ability, Water Absorb? Water Absorb would block Tentacruel's Scald, and Tentacruel is in 15 to 19 of the screen's top 20 sixes on boxes 1 and 2.
5. If he takes Toxicroak, its nature (I used Adamant, which no other member has) and whether its Sucker Punch should be Ice Punch, so that it does not share Pawmot's move.

**Next steps.** Ian answers in a line each. Then a session applies the chosen slot and the egg-list edits on this branch and reruns the legality check and the outcome probe below, which takes about an hour. A spot-check reading happens only if Ian names one, and takes two and a half to four hours.

## Part 1: what could invalidate the fight

### Legality

The Kaizo study's checker, with the pre-TM-pass TM lists, finds these off-list moves. The OxiDex's own list agrees, except that it also flags Cacturne's Fling, because it reads only today's TMs. Fling was Cacturne's TM before the TM pass, so it stays in the trainer palette (Ian, 2026-10-07).

| Member | Move | Where Oxide has it | Where canon has it |
|---|---|---|---|
| Pawmot 37 | Sucker Punch | nowhere | nowhere |
| Pawmot 37 | Volt Switch | nowhere | Generation 9 TM |
| Heracross 36 | Close Combat | Heracross's level 37 | Generation 4 level 37 |
| Heracross 36 | Bug Bite | nowhere | Generation 4 tutor, Generation 9 TM |
| Hakamo-o 38 | Dragon Dance | Hakamo-o's level 66 | Generation 9 level 44 and TM |
| Hakamo-o 38 | Focus Punch | nowhere | Generation 9 TM |

Every other move is legal. Medicham's Psycho Cut and Fire Punch are egg moves. Lucario's Aura Sphere is its level 37 move and Vacuum Wave an egg move. Cacturne's Revenge is a level 1 move and Seed Bomb an egg move. Hakamo-o's Counter is its level 29 move and Outrage a TM.

### The rest of the rulings

These pass, and none needs a decision:

- Items: no item repeats. Each item works in the simulator and has a holder it suits. In the outcome probe Heracross was burned in 91 to 123 of 150 fights, and Cacturne threw its Iron Ball in 21 to 98. Pawmot's Payapa Berry went in 2 to 27, the most on box 3, where Delphox carries Psyshock. The Eviolite applies, because Hakamo-o still evolves.
- Natures: no nature repeats.
- Abilities: Volt Absorb, Guts, Pure Power, Overcoat and Adaptability all work with their sets, and the boxes carry Electric moves for Volt Absorb to stop. The exception is Sand Veil, in question 4.
- Members under their evolution levels: Medicham is one level under Meditite's 37, which is fine. Hakamo-o is past Jangmo-o's 35 and under Kommo-o's 45, a middle stage at its own level. Pawmot comes from a Thunderstone, and Lucario is past Riolu's 28.
- Banned moves: no one-hit KO move, no evasion move and no trapping move. The team carries no forced trade, where Maylene may have one.

The simulator models every unusual piece of this team. Counter returns physical damage only. Focus Punch fails when its user is hit first. Fling spends the held item and fails without one. Iron Ball halves Speed until the ball is gone. I found no gap to report.

### The new AI flags

Risky adds 2, half the time, to Counter, Focus Punch, Revenge, Payback, Sucker Punch and the high-critical-hit moves, which takes in Psycho Cut. Prioritize Extremes adds 2, 60.9 percent of the time, to every status move and to the moves the damage check skips: Counter, Fling, Focus Punch and Sucker Punch. That covers eight of Maylene's 24 moves. Three effects show in the probe. Medicham uses Psycho Cut far more than its 130-power High Jump Kick (118 to 253 uses against 12 to 139). Pawmot's Sucker Punch is used 152 to 274 times a run and lands 91 to 94 percent of the time, though only because the probe's greedy player always attacks; a real player can bait it with a status move. Hakamo-o's picks are covered in Part 2. None of this breaks the fight. The Hakamo-o effect is why its slot is the crux.

## Part 2: the weakest crux

### Pawmot passes the bait test

Ian's test is that a lead may be fully countered, so long as the counter draws in something that beats it, ideally with setup the player has to switch against. I traced the AI's replacement rule (`fightai.replacement`, the engine's BattleAI_PostKOSwitchIn, which Volt Switch's pivot also uses) against every catch the screen's top 20 sixes take five or more times. Each of Pawmot's answers draws a member that beats it:

| Pawmot's answer (margin on Pawmot) | Drawn in | That member on the answer |
|---|---|---|
| Bastiodon (+3.0), Probopass (+3.0), Garganacl (+2.5) | Lucario | Aura Sphere 168 to 204 percent on Bastiodon, 160 to 192 on Garganacl |
| Ninetales-Alola (+3.0), Granbull (+0.5) | Lucario | Flash Cannon 248 to 296 percent on Ninetales-Alola, 192 to 228 on Granbull |
| Bronzong (+2.5), Tentacruel (+0.5) | Medicham | Medicham wins both one-on-ones by the screen (each has a margin of -1.5 on it) |

The drawn member has no setup move, which is the one part of the test Pawmot misses. Lucario is the first member in after the lead in 48 to 102 of 150 fights. The team's only setup move sits on Hakamo-o, which the rule sends in against two catches only: Staraptor, after Pawmot leaves, and Bronzong, after Medicham leaves.

### Why Hakamo-o's slot is the crux

The probe numbers below come from five runs of 150 fights each, on goal 3's three boxes. Box 2's two sixes were the same six, which is why there are five runs and not six.

| | Pawmot | Heracross | Medicham | Cacturne | Hakamo-o | Lucario |
|---|---|---|---|---|---|---|
| Player's Pokemon knocked out while it was in | 64 to 100 | 50 to 173 | 104 to 243 | 50 to 116 | 19 to 60 | 158 to 248 |

The weakness is not its number of answers: four to seven catches beat Hakamo-o, as few as beat Medicham, and only Lucario has fewer. It comes from three other things.

1. The AI picks Counter most, 71 to 102 times a run, against Outrage's 21 to 63. Counter and Focus Punch both move last, so Hakamo-o is often knocked out before they go. Of the moves it got off, Counter took HP 7 to 23 times a run and Focus Punch 0 to 5. Dragon Dance went off 12 to 41 times, but an Outrage followed it only 0 to 7 times. The greedy player always attacks, so Focus Punch fares worse here than against a careful player. A careful player, though, would also send a special attacker into Counter.
2. Hakamo-o is four times weak to Fairy, and the three Fairies the screen takes most each knock it out in one hit from full HP. Togetic's Dazzling Gleam does 112 to 136 percent, Ninetales-Alola's 144 to 172, and Granbull's Spirit Break 100 to 124. Outrage cannot touch them, and its Fighting moves are resisted. Togetic is in 14 to 16 of the top 20 sixes on every box, at a margin of +3.0 on Hakamo-o.
3. Being the team's one setup member, it should be the one that Pawmot's and Medicham's answers draw in, and it almost never is (above).

### The picks

Each set keeps Ian's other five members as they stand. Each pick was swapped in memory and run through the screen, the replacement trace and the outcome probe on the same three boxes, six runs of 150 fights each.

| Set | Legal | Knocked out while in | Setup used, per run | Who draws it in | Its answers in the top sixes |
|---|---|---|---|---|---|
| Ian's: Hakamo-o 38, Eviolite, Lax, Overcoat; Counter, Dragon Dance, Focus Punch, Outrage | two moves off-list | 19 to 60 | Dragon Dance 12 to 41, Outrage after it 0 to 7 | Staraptor, Bronzong | Togetic +3.0, Granbull +2.5, Ninetales-Alola +1.5 |
| 1. Toxicroak 38, Black Sludge, Adamant, Dry Skin; Swords Dance, Poison Jab, Drain Punch, Sucker Punch | yes | 78 to 169 | Swords Dance 57 to 89 | Granbull on every box; Ninetales-Alola after Lucario; Breloom after Medicham | Tentacruel +1.5 (20 of 20 on boxes 1 and 2), Delphox +1.5 (20 of 20 on box 3) |
| 2. Hakamo-o 38, Eviolite, Lax, Overcoat; Bulk Up, Drain Punch, Outrage, Rock Slide | yes | 31 to 103 | Bulk Up 47 to 105, Outrage after it 11 to 33 | Staraptor | Granbull +3.0, Ninetales-Alola +2.5, Togetic +1.5 (1 to 2 of 20) |
| 3. Hakamo-o as pick 2, with Dragon Dance for Bulk Up | Dragon Dance off-list | 37 to 104 | Dragon Dance 38 to 85, Outrage after it 16 to 37 | Staraptor | the same as pick 2 |

Toxicroak is my first pick because it is the only one that meets Ian's bait test. Pawmot's answer Granbull draws it in on every box, and its Poison Jab does 108 to 128 percent to Granbull and 104 to 126 to Ninetales-Alola. It carries Swords Dance at 1 PP, and the player has to switch against it. Its own answers are Tentacruel (Psybeam 96 to 116 percent, at Speed 88 against its 81) and Delphox, and Dry Skin turns Tentacruel's Scald to nothing. The price is size: it more than doubles the slot's output and comes near Lucario's, so the fight gets clearly harder, and the team loses its Dragon type. Every move is legal: Swords Dance through the pre-TM-pass TM, Poison Jab at Croagunk's level 38, Drain Punch and Sucker Punch on its own lists.

Pick 2 keeps Ian's member, item, nature and ability, and fixes the slot with legal moves only. Bulk Up (3 PP) is reliable setup, Drain Punch keeps an Eviolite holder healthy, and Rock Slide hits Togetic super-effectively. That takes Togetic from 14 to 16 of the top 20 sixes down to 1 or 2. It does not fix the Fairy weakness or the replacement rule: Granbull and Ninetales-Alola still knock it out in one hit.

Pick 3 is pick 2 with Ian's Dragon Dance kept, for the Speed. Its knockouts are within seven of pick 2's in every run, and it needs Dragon Dance added to an egg list.

## How the numbers were made

Every number comes from a run in the worktree at 0d358a4505. The scratch scripts are in `/home/ian/.claude/jobs/382760ce/tmp/maylene/`, each with its own usage line, and none writes to `res/`.

- The boxes and the matchup screen come from `plgoal3 --run maylene-study --box maylene <seed> --screen` for seeds 1 to 3. The run name has no earlier results.
- Margins, Speeds and damage come from Fantina's `margins.py` and `probe.py`, pointed at `maylene`. The rows now hold percent of HP, so `probe.py` prints them as they are. `tally.py` counts the catches with a positive margin on each member. Damage is the calculator's lowest to highest roll at no stat stages.
- The AI-picks probe is `probe.py`: rough fights against a greedy player, on two sixes per box (the screen's best and its most common). Its win and faint numbers mean nothing.
- `outcome.py` replays the same fights and counts what each move did. It counts a move only when the member was standing when its turn came, and it ignores the moves the player's replacement look-ahead tries out. It also counts burns, flung items and the first member in after the lead.
- `replace.py` runs `fightai.replacement` for each member leaving, against each catch.
- `ironball.py` reads Cacturne's simulated Speed before and after the fling.
- `swap.py CANDIDATE SCRIPT SEED` swaps a pick into Hakamo-o's slot in memory, as Fantina's `lead.py` did, then runs one of the scripts above.
- Legality comes from `oxide.py check 39`, with `OXIDE_OLD_RES` set to an export of 5c62989651's `res/`, and from `legal.py`, which uses the OxiDex's `learnsets.lists`. `palette.py` lists a species' legal moves at a level.

Where the screen's bias bites: it counts only a clean one-on-one from full HP with no status move. So it reads picks 2 and 3 as identical. It never sees Counter. And it counts Focus Punch as a sure hit, which is why it rates Ian's Hakamo-o better against Ninetales-Alola (+1.5) than the fixed sets (+2.5), although Focus Punch took HP at most five times a run in play. It also counts no paralysis from Nuzzle and no confusion from Water Pulse. The probe's greedy player never uses a status move, which flatters Pawmot's Sucker Punch and hurts Focus Punch.

## Hakamo-o's slot, against Flying types (2026-10-31)

Ian asked on 2026-10-31 for Hakamo-o's slot to go to something that patches the team's weakness to Flying types and adds a little bulk, but not much, since the team is frail on purpose. It need not be a Fighting type, so long as it carries a Fighting move or fits the theme. The other five stay as they are. Every number here was made on `origin/oxide` at ad7ea90c4, with Water Absorb on Cacturne, by cheap checks only. Nothing in `res/` changed.

### Summary

**Outcome.** The worry is real but narrow. The only Flying catch the screen takes often is Togetic (14 to 16 of the top 20 sixes on every box), and it is taken for its Fairy moves against Hakamo-o, not for its Flying ones. The Flying attackers proper (Staraptor, Golbat, Talonflame) are in 0 to 7 of the 20, but each beats Heracross, and Staraptor also beats Medicham, Cacturne and Hakamo-o one on one. Any of the four picks below drops Togetic to 0 to 3 of the 20. Each also more than doubles what the slot knocks out, so the fight gets harder whichever is taken: Hakamo-o knocked out 15 to 60 of the player's Pokemon per 150 rough fights, and every pick knocks out 44 to 165.

**My first pick is Garganacl** (level 38, Hard Stone, Adamant, Purifying Salt: Curse, Hammer Arm, Rock Slide, Salt Cure). It resists Flying and Normal, and its Rock Slide knocks out Staraptor, Golbat and Talonflame from full HP (122 to 146 percent on Staraptor) and nearly does Togetic (104 to 126). It is 10 percent bulkier than Eviolite Hakamo-o physically and 22 percent specially, with no Eviolite. Purifying Salt makes it immune to every major status, so Scald's burn and Will-O-Wisp cannot cripple it. Its Curse went off 128 to 164 times a run, against Dragon Dance's 11 to 39, so the team's setup now gets used. The Flying catches facing Pawmot or Medicham draw it in, and it beats all of them except Staraptor with Close Combat, which wins by half a point. Every move is legal with no egg-list edit. The theme is the sumo ring, where salt is thrown before a bout, with Hammer Arm as its Fighting move.

**The other picks, in order.**

1. Lairon with Eviolite (Lonely, Rock Head: Rock Polish, Iron Head, Rock Slide, Superpower). It is the only set that passes Ian's bait test for Pawmot: the Fairy answers, Ninetales-Alola and Granbull, draw Lairon in, and its Iron Head does 184 to 220 percent to Ninetales-Alola and 96 to 114 to Granbull, with Rock Polish behind it. It quarter-resists Flying and resists Fairy. The price is a fourfold weakness to Fighting and Ground: the player's Heracross (20 of 20 sixes on box 2) knocks it out with Close Combat, and so does Staraptor's. Its only Fighting move is Superpower, so the theme is thin. Its output swings the most, 44 to 165.
2. Graveler with Eviolite (Naughty, Sturdy: Rock Polish, Hammer Arm, Rock Slide, Earthquake). It resists Flying, takes almost nothing from the Flying moves, and Pawmot's answer Tentacruel draws it in, which it beats only through Sturdy (Scald does 108 percent, capped at 1 HP) and then Earthquake. A Scald after any chip, or a burn, ends it.
3. Sudowoodo (Passho Berry, Relaxed, Rock Head: Wood Hammer, Rock Slide, Drain Punch, Ice Punch). It resists Flying, but its bulk is Hakamo-o's own (1.00 and 1.02 times), and it carries no setup, so the team loses its only setup member.

Electabuzz and Dusknoir were checked and are not picks. Electabuzz with Eviolite is 30 percent frailer physically, the replacement rule never sends it in, and it knocked out the most of any pick but Dusknoir (119 to 268). Dusknoir is far bulkier than asked (1.76 times Hakamo-o's special bulk): no catch in any top 20 beats it one on one, and it knocked out 207 to 283, more than Lucario.

**What Ian decides.**

1. Which set takes the slot: Garganacl, Lairon, Graveler, Sudowoodo, or Hakamo-o after all.
2. Whether the rise in what the slot knocks out is acceptable. It is a material difficulty change for Maylene's fight whichever pick he takes, since the slot goes from the team's weakest member to its second or third strongest.
3. For Garganacl, whether Curse is the setup he wants, or Iron Defense, its other legal setup move. Curse takes Garganacl's Speed down, which suits a member at 43 Speed that moves last anyway.

**Next steps.** Ian answers in a line. A session then writes the chosen set into `leader_maylene.json` on a branch, reruns the legality check and the outcome probe on all three boxes (about 30 minutes), and lands it through the Overseer. A spot-check reading happens only if Ian names one, and takes two and a half to four hours.

| Set | Legal | Bulk beside Hakamo-o (physical, special) | Worst Flying catch's damage on it | Its damage on that catch | Knocked out while in | Setup used, per run | What draws it in |
|---|---|---|---|---|---|---|---|
| Ian's: Hakamo-o 38, Eviolite, Lax, Overcoat; Counter, Dragon Dance, Focus Punch, Outrage | yes (Dragon Dance and Focus Punch on the egg lists) | 1.00, 1.00 | Togetic, Dazzling Gleam 112 to 136 | Focus Punch 15 to 18 | 15 to 60 | Dragon Dance 11 to 39 | Staraptor after Pawmot; Bronzong and Vikavolt after Medicham |
| 1. Garganacl 38, Hard Stone, Adamant, Purifying Salt; Curse, Hammer Arm, Rock Slide, Salt Cure | yes | 1.10, 1.22 | Staraptor, Close Combat 64 to 76 | Rock Slide 122 to 146 | 124 to 151 | Curse 128 to 164 | Togetic, Golbat, Staraptor, Talonflame after Pawmot or Medicham; Delphox, Salazzle, Vikavolt on box 3 |
| 2. Lairon 38, Eviolite, Lonely, Rock Head; Rock Polish, Iron Head, Rock Slide, Superpower | yes | 1.23, 0.91 | Staraptor, Close Combat 88 to 108 | Rock Slide 96 to 114 | 44 to 165 | Rock Polish 52 to 106 | Ninetales-Alola and Granbull after Pawmot or Medicham; Golbat, Togetic, Talonflame, Staraptor, Cinderace, Vikavolt |
| 3. Graveler 38, Eviolite, Naughty, Sturdy; Rock Polish, Hammer Arm, Rock Slide, Earthquake | yes | 1.24, 1.03 | Togetic, Magical Leaf 60 to 72 | Rock Slide 86 to 104 | 93 to 149 | Rock Polish 62 to 100 | Tentacruel after Pawmot or Medicham; Talonflame, Staraptor, Cinderace, Delphox, Salazzle, Vikavolt |
| 4. Sudowoodo 38, Passho Berry, Relaxed, Rock Head; Wood Hammer, Rock Slide, Drain Punch, Ice Punch | yes | 1.00, 1.02 | Staraptor, Close Combat 66 to 78 | Rock Slide 102 to 122 | 119 to 157 | none | Golbat, Staraptor, Talonflame, Togetic, Leavanny, Cinderace; Delphox and Salazzle on box 3 |
| Not a pick: Electabuzz 38, Eviolite, Jolly, Static; Bulk Up, Thunder Punch, Cross Chop, Ice Punch | yes | 0.70, 1.41 | Staraptor, Take Down 55 to 66 | Thunder Punch 102 to 122 | 119 to 268 | Bulk Up 85 to 152 | nothing |
| Not a pick: Dusknoir 38, Spell Tag, Hardy, Levitate; Shadow Punch, Ice Punch, Brick Break, Will-O-Wisp | yes | 1.17, 1.76 | Staraptor, Brave Bird 55 to 66 | Ice Punch 78 to 94 | 207 to 283 | none | Dusclops; Rotom, Cofagrigus, Bronzong, Delphox, Vikavolt |

Damage is percent of the target's HP, lowest to highest roll, at no stat stages. "Knocked out while in" and "setup used" span the five or six probe runs of 150 fights each (two sixes a box, one where both are the same six). Lucario, for scale, knocked out 94 to 257 in the same runs.

### The evidence

Oxide's types match the count in the brief. Heracross (Bug and Fighting) takes four times from Flying; Medicham (Fighting and Psychic), Cacturne (Grass and Dark) and Hakamo-o (Dragon and Fighting) twice; Pawmot (Electric and Fighting) and Lucario (Fighting and Steel) take neutral damage.

These are the Flying catches the screen's top 20 sixes take with Hakamo-o in the slot, and their margins on each of the six (positive means the catch wins one on one from full HP):

| Catch | Box 1 | Box 2 | Box 3 | Pawmot | Heracross | Medicham | Cacturne | Hakamo-o | Lucario |
|---|---|---|---|---|---|---|---|---|---|
| Togetic (Fairy and Flying) | 14 | 15 | 16 | -0.5 | +1.5 | -0.5 | +1.5 | +3.0 | -2.5 |
| Staraptor, Dual Wingbeat | 4 | 5 | not in box | -0.5 | +1.5 | +1.5 | +0.5 | +0.5 | -0.5 |
| Staraptor held to 37, Brave Bird | 3 | 2 | not in box | -0.5 | +1.5 | +1.5 | +1.5 | +1.5 | -0.5 |
| Golbat | 2 | 5 | 2 | -1.5 | +2.5 | -0.5 | +0.5 | -0.5 | -2.5 |
| Talonflame | 2 | not in box | not in box | -1.5 | +2.5 | +0.5 | +0.5 | -1.5 | -0.5 |
| Heracross with Aerial Ace | not in box | 15 | not in box | +0.5 | +0.5 | -0.5 | +2.5 | -0.5 | +0.5 |

The Flying moves themselves, on the six:

| Move | Pawmot | Heracross | Medicham | Cacturne | Hakamo-o | Lucario |
|---|---|---|---|---|---|---|
| Staraptor's Brave Bird | 88 to 104 | 412 to 492 | 186 to 222 | 168 to 198 | 96 to 114 | 93 to 109 |
| Staraptor's Dual Wingbeat | 48 to 60 | 240 to 288 | 108 to 132 | 96 to 112 | 60 to 72 | 50 to 62 |
| Golbat's Dual Wingbeat | 36 to 44 | 168 to 200 | 76 to 96 | 64 to 84 | 40 to 52 | 36 to 44 |
| Talonflame's Aerial Ace | 26 to 32 | 124 to 148 | 56 to 68 | 50 to 62 | 30 to 36 | 28 to 34 |
| Togetic's Air Cutter | 32 to 38 | 96 to 112 | 56 to 68 | 50 to 60 | 44 to 54 | 27 to 33 |

Corvisquire and Vullaby are each in one six on box 3 and beat nobody but Heracross or Cacturne. A Staraptor with Brave Bird knocks out Heracross, Medicham and Cacturne from full HP, and Pawmot, Hakamo-o and Lucario on a high roll. Togetic's Air Cutter does little except to Heracross; Togetic is in the sixes for Dazzling Gleam, which does 112 to 136 percent to Hakamo-o. With any of the picks in the slot, the screen stops taking Togetic (0 to 3 of 20) and takes more Golbat and Staraptor instead, which the Rock types beat, the Close Combat Staraptor apart. The player's own Heracross, on box 2, goes from 15 to 20 of 20 sixes against the Rock types, by Close Combat.

### The candidates

The whole Pokedex was screened (`dexscreen.py`, below): every species Oxide has that can be fielded at 38, resists Flying or has a legal Rock, Electric or Ice move of 50 power or more, and has a legal Fighting move, with its bulk at 38 beside Eviolite Lax Hakamo-o's. Bulk is HP times Defence and HP times Special Defence, with the nature and the Eviolite.

Most of the species the brief named are not in Oxide: Golett and Golurk, Eelektrik and Eelektross, Crabominable, Tyrunt and Tyrantrum, Boldore and Gigalith, Cufant and Copperajah, Stonjourner and Beartic. Of the rest:

| Species | Why it is in or out |
|---|---|
| Garganacl | in: resists Flying, bulk 1.10 and 1.22 at a neutral nature, Hammer Arm and Rock Slide legal |
| Lairon | in: quarter-resists Flying, resists Fairy, Eviolite bulk 1.37 and 0.90 at a neutral nature |
| Graveler | in, an addition: resists Flying, Eviolite bulk 1.24 and 1.15, Hammer Arm and every punch legal |
| Sudowoodo | in: resists Flying, bulk 0.91 and 1.01 at a neutral nature, the least bulk of the Rock types |
| Electabuzz | tested: resists Flying, Eviolite bulk 0.69 and 1.41, Bulk Up and the elemental punches legal |
| Dusknoir | tested, an addition and the nearest stand-in for Golurk's punches: bulk 1.17 and 1.76 |
| Electivire | out: 0.55 physical bulk |
| Ampharos | out: 0.66 physical bulk, though it would have kept the Dragon type |
| Hawlucha | out: takes double from Flying, 0.61 physical bulk |
| Aggron | out: Lairon evolves at 42 |
| Bastiodon, Probopass, Bronzong, Steelix, Magneton | out: no legal Fighting move at 38, and the first three are already common catches in the box |
| Corviknight | out: a Flying type itself, with only Revenge as a Fighting move |
| Machoke, Primeape, Hitmonchan, Toxicroak, Mienshao | out: Fighting types, double weak to Flying, so they add to the problem |
| Vigoroth, Lopunny, Piloswine | out: neutral to Flying and off the theme, or nearly so; Lopunny also takes the Eviolite through its Fist Plate evolution, which would be an accident |

### The sets

Each set is level 38 with an item and a nature no other member uses, and each was checked legal by both checkers (the Kaizo study's palette with the pre-TM-pass TMs, and the OxiDex's `learnsets.lists`). None needs an egg-list edit. None carries a one-hit KO move, an evasion move, a trapping move, a Choice item or a forced trade. Garganacl, Lairon and Graveler keep a setup move (Curse, Rock Polish, Rock Polish), and I checked that the simulator applies Curse's +1 Attack, +1 Defence and -1 Speed and Rock Polish's +2 Speed. Sudowoodo and Dusknoir have none. Garganacl's Hard Stone and Sudowoodo's Passho Berry stand where a Leftovers would have added more bulk than Ian wants.

Under Ian's lead rule, Pawmot's answers (Bastiodon, Probopass, Garganacl, Ninetales-Alola, Granbull, and Tentacruel on boxes 1 and 2) still draw in Lucario with Garganacl, Graveler or Sudowoodo in the slot. With Lairon, Ninetales-Alola and Granbull draw in Lairon instead, which beats both and carries Rock Polish, so Pawmot meets the rule in full. With Graveler, Tentacruel draws in Graveler, which beats it narrowly. When Medicham leaves, its answers draw the same members as Pawmot's, except the Flying catches: with Hakamo-o they drew in Pawmot, and with the Rock types most of them draw in the slot instead (Togetic, Golbat and Staraptor draw Garganacl; Togetic, Golbat and Talonflame draw Lairon).

### How the numbers were made

The scripts and their outputs are in `/home/ian/.claude/jobs/382760ce/tmp/maylene-slot/`, copied from the 2026-10-29 folder, each with its own usage line; none writes to `res/`. They ran in the worktree `.claude/worktrees/maylene-slot` on branch `overseer-maylene-slot` at ad7ea90c4.

- `swap.py CANDIDATE SCRIPT SEED` swaps a set into slot 4 in memory, as before. The new sets are in its `CANDS`.
- `flying.py` lists every Flying-typed catch, or catch with a Flying move, in each box, with its top-20 count, margins and damage both ways.
- `duel.py` gives damage both ways and the margin between the slot and the box's main catches.
- `margins.py`, `outcome.py` and `replace.py` are the 2026-10-29 scripts. `replace2.py` is `replace.py` widened to every catch the top 20 take twice or more, so that the Flying catches show.
- `dexscreen.py` is the whole-Pokedex screen; `legal_cands.py` is the OxiDex's legality check for each set; `cursecheck.py` checks the setup moves' stages.
- `summarise.py` gathers the table's numbers from the outputs.

The screen's biases from the 2026-10-29 study still hold: one-on-one from full HP, no status moves, and a greedy probe player who always attacks. Two matter here. The screen counts Graveler's Sturdy as a sure survival, which a careful player breaks with any chip first. And the greedy player never switches against Curse or Rock Polish, so the setup and knockout numbers for the picks run high against a real player.

# Maylene's six: a short check

Ian built Maylene's six (Veilstone Gym, Maylene's split, cap 39) in the OxiDex on 2026-10-29 and asked for two things only: anything that invalidates the fight, and the weakest crux with the top replacement picks for it. His natures are his choice and are not argued here. The six is on branch `overseer-maylene` (0d358a4505) for study only; nothing here lands.

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

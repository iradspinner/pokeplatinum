# Four AI flags, and when a team should carry them

Ian asked on 2026-10-31 for the AI flags to be set on purpose for each team, and for four of them to be understood closely: Check HP with Explosion and Self-Destruct, Weather with a lead that carries a weather move, Harassment with a team of status moves, and Risky with high-critical-hit moves. This guide says what each flag does to those moves, from the script as it stands (`src/battle/trainer_ai/script.s`, read by label, since its line numbers move). The engine, and the rest of each flag, are in this folder's README and `other-flags.md`. Nothing in the script was changed for this guide.

## How to read the numbers

Every move starts a turn at 100, each flag's routine adds to or takes from it, and the highest score is used, ties broken at random. Almost every Oxide trainer runs Basic, Evaluate Attack and Expert. Under Evaluate Attack the strongest damaging move keeps its score, every weaker damaging move loses 1, and a move that would knock the target out gains 4. A status move gets no damage comparison, so it keeps its score too.

The chances below are worked out from the script's own numbers. They are the chance that the move named beats the trainer's best attack, with that attack left at its starting score and nothing else in play: no kill on the board, no super-effective bonus from Expert. They show how each flag moves the odds, not what a whole fight will do. "Base" means Basic, Evaluate Attack and Expert alone.

A random check in the script draws 0 to 255. The chances that recur here are 80.5 percent (a check against 50), 50 percent (against 128) and 60.9 percent (against 100).

## Check HP, with Explosion, Self-Destruct and Destiny Bond

Check HP keeps a Pokemon off moves that suit a different HP, its own and the target's (`CheckHP_Main`). It takes 2 from the move, 80.5 percent of the time, when the move's effect is in the table for the user's HP band, and 2 more, again 80.5 percent of the time, when it is in the table for the target's band. The bands are above 70 percent, 31 to 70 percent, and 30 percent or less.

Explosion and Self-Destruct share one effect. It is in the user's tables above 70 percent and from 31 to 70 percent, but not at 30 percent or less, and in the target's table at 30 percent or less. So Check HP discourages exploding while the user is healthy, never once it is at 30 percent or less, and always when the target is nearly down already. Destiny Bond sits only in the user's table above 70 percent.

Without Check HP, Explosion is already shaped by two flags. Evaluate Attack takes 2 from it, 80.1 percent of the time, since it never counts as a kill (`EvalAttack_Main`). Expert scores it by the user's HP (`Expert_Explosion`): minus 3 at 80 percent or more if the user is faster, minus 1 above 50 percent, a 50 percent chance of plus 1 from 50 down to 31, and up to plus 2 at 30 percent or less. Basic forbids it outright into a Ghost, into Damp, or from the last Pokemon when the target has more.

Explosion's chance against the best attack, the user slower, the target above 30 percent:

| User's HP | Base | With Check HP | With Risky | With Check HP and Risky |
|---|---:|---:|---:|---:|
| above 80% | 2% | 0% | 15% | 4% |
| 51 to 80% | 2% | 0% | 15% | 4% |
| 31 to 50% | 15% | 3% | 47% | 15% |
| 30% or less | 35% | 35% | 66% | 66% |

A faster user above 80 percent explodes 2 percent of the time on the base flags and 0.4 percent with Check HP. With the user at 30 percent or less and the target at 30 percent or less too, Check HP holds Explosion to 10 percent.

What this means in a fight: with Check HP a trainer's exploder waits until it is at 30 percent or less, and then goes about one turn in three. A Custap Berry fires at a quarter of maximum HP, so a Custap exploder with Check HP is unlikely to explode before the berry is in range, and the player plays round it by knocking it out from above 30 percent in one hit, or by leaving it at 31 to 50 percent, where it is least likely to go. Without Check HP it explodes now and then from the middle band, which reads as random.

Destiny Bond is a status move, so Evaluate Attack leaves it alone. Expert takes 1 from it, and, only if the user is faster, adds a 50 percent chance of plus 1 at 70 percent or less, another at 50 percent or less, and a 60.9 percent chance of plus 2 at 30 percent or less (`Expert_DestinyBond`). A slower user never uses it on the base flags. Its chance against the best attack, the user faster:

| User's HP | Base | With Check HP | With Risky |
|---|---:|---:|---:|
| above 70% | 0% | 0% | 50% |
| 51 to 70% | 25% | 25% | 62% |
| 31 to 50% | 50% | 50% | 75% |
| 30% or less | 80% | 80% | 90% |

With Check HP and Risky together, a healthy faster user bonds 10 percent of the time. So Check HP changes Destiny Bond only above 70 percent, and only when Risky is also on. The player plays round Destiny Bond with status, or by not striking the last blow while it is up.

Check HP also discourages setup moves (every one- and two-stage raise, Dragon Dance and its family, Calm Mind, Bulk Up and Belly Drum) at 70 percent or less, and healing moves above 70 percent. On a team with setup or healing it makes those moves better timed.

The rule for a team: a team whose idea uses Explosion, Self-Destruct or Destiny Bond carries Check HP, so the trade move lands where a player can see it coming.

## Weather, with a lead that carries a weather move

Weather now does one thing (`Weather_Main`; the vanilla bug that gave every move the same bonus was fixed on 2026-09-22). On the battle's first turn only, and on the user's own first turn, Sunny Day, Rain Dance, Sandstorm and Hail gain 5 if that weather is not already up. Every other move gains nothing, and from turn 2 on the flag does nothing at all.

Plus 5 beats a kill's plus 4 and nearly anything else a first turn can score, so a lead with a weather move and this flag sets its weather on turn 1 almost every time. A Pokemon sent in later never gets the bonus. A weather ability (Drizzle, Drought, Sand Stream, Snow Warning) needs no flag, and the flag does nothing for a team whose only weather comes from an ability.

The rule for a team: Weather goes only on a team whose lead carries a weather move it should open with. On any other team it does nothing, so it is left off.

## Harassment, with status moves

Harassment adds 2, 50 percent of the time, to every move whose effect is in its table (`Harrassment_Main`). The table holds sleep, Yawn, poison (Poison Powder, not Toxic), paralysis (Thunder Wave, Stun Spore, Glare), burn (Will-O-Wisp), confusion, Swagger and Flatter, attraction, Leech Seed, Encore, Spite, Torment, the one- and two-stage stat drops, Spikes, Toxic Spikes and Sticky Web, Defog, Embargo and Magic Room, Psycho Shift, and two attacks, Knock Off and Ceaseless Edge. Toxic, Stealth Rock and Taunt are not in it.

A status move keeps its starting score under Evaluate Attack, so on the base flags it already ties the best attack, and wins half those ties, wherever Expert leaves it alone. Harassment lifts that to 75 percent. Expert still stops a move that cannot work, such as Thunder Wave on a Ground type or a second Spikes once three layers are down, since those penalties are far larger than 2.

The rule for a team: Harassment goes on a team whose idea is status or hazards, carrying at least two of the table's status moves, so that it opens with them and keeps reapplying them instead of attacking.

## Risky, with high-critical-hit moves

Risky adds 2, 50 percent of the time, to every move whose effect is in its table (`Risky_Main`). For critical hits the table holds only the plain high-critical effect, which in Oxide is Stone Edge, Night Slash, Psycho Cut, Leaf Blade, X-Scissor, Shadow Claw, Slash, Crabhammer, Drill Peck, Drill Run, Dragon Claw, Cross Chop, Karate Chop, Megahorn, Power Whip, Aqua Cutter, Air Cutter, Razor Leaf, Snipe Shot, Aeroblast and Spacial Rend. Cross Poison, Poison Tail, Blaze Kick and Esper Wing carry their own effects and are not in it, though Expert scores them as below. The table also holds Explosion and Self-Destruct, Destiny Bond, Counter, Mirror Coat, Metal Burst, sleep, confusion, Swagger, Sucker Punch, Gyro Ball, Avalanche, Payback, Belly Drum, Ancient Power and Final Gambit.

Expert already gives a high-critical move a 50 percent chance of plus 1 when it is super effective, and a 25 percent chance when it is neutral (`Expert_HighCritical`). A high-critical move that is not the trainer's strongest therefore beats the strongest:

| The high-critical move against the target | Base | With Risky |
|---|---:|---:|
| super effective | 25% | 62% |
| neutral | 12% | 56% |
| resisted | 0% | 50% |

When the high-critical move is already the strongest, Risky changes little. So Risky makes a crit team reach for its crit moves even when another move would do more damage. It also makes every other gamble in the table more likely, Sucker Punch and Counter among them.

The rule for a team: Risky goes on a team whose idea is critical hits (Super Luck, Sniper, a Scope Lens or Razor Claw behind high-critical moves). It is kept off a team that carries a trade move unless that team should spend it freely.

## One flag more: Prioritize Extremes

Prioritize Extremes adds 2, 60.9 percent of the time, to every move without a damage comparison: every status move, and Explosion, Self-Destruct, Sucker Punch, Head Smash, Solar Beam, Eruption, Focus Punch and the like. It pushes the same moves as Harassment and Risky together, but without telling a team's idea apart from its filler, so a team that wants one of those pushes carries the flag for it instead.

# How the scorer reads a fight (2026-10-03)

This is the scoring track's plain account of what a reading is, for anyone
who uses the numbers without the machinery: the Kaizo study, the balance
passes, Ian. The detail and the measurements behind each choice are in
[the scoring handoff](trainer-scoring-handoff.md).

**The battle.** Each fight is played out in a simulator of Oxide's battle
engine. The trainer's side is played by a port of the game's own battle AI,
routine by routine from the decomp, with a test for each; where the AI's
scores tie, it picks at random, as the game does. Damage comes from the
damage calculator with Oxide's move numbers. Every chance (a crit, a
secondary status, a miss, a full paralysis) is rolled at the game's real
odds. The player uses no items in battle. Held items come from what the run
can have by then: a type booster for a member's main attack, then Leftovers
or a Sitrus Berry while copies last.

**The player.** Each turn the scorer looks at every option it has (each
move, each switch). For each, it plays the turn against every pick the
trainer's AI could make, weighted by how likely the AI is to make it, and
against the turn's dice. Then it plays each resulting position on to the
end many times with a simple stand-in player (knock out what it can, switch
once into a matchup it wins, otherwise attack with its strongest move), 64
play-outs per option and trainer pick, and counts how those end. It chooses
the option with the lowest chance of losing the fight, counting chances
within five points as equal; among those, the fewest Pokemon fainting;
among those, the best position. Nothing tells it to stall, bait or pivot;
those plays come out of this look-ahead on their own, and the three-gym
run's planning ideas are the test of whether they do.

**The six.** An ordinary trainer is read blind: each of its simulated fights
draws its own six at random from the stronger half of a realistic box,
never a member held below the cap (Ian, 2026-10-04). The stronger half is
judged without the trainer in view, by how each member fares on paper
against the split's other ordinary trainers with its own moves, so the
player brings the Pokemon it relies on that split, not a six chosen for
this fight. For a
boss the scorer picks its own six and moves from the box. It first scores
every possible six on paper (who knocks out whom, in how many hits, who
moves first), choosing each member's four moves for this fight. A fast,
rough learned judge then races the promising sixes against each other. The
best three are read properly by the scorer above, and the best of those is
improved: the enemies that made it lose Pokemon point to the box members
that answer them, and sixes built with those are read too. The best six by
wins, then faints, is the boss's six.

**The reading.** A fight is read on 100 simulated fights: 75 at real odds and
25 very unlucky, where every crit and status check rolls twice and keeps
the result worse for the player. It gives three numbers: the win rate (won
at all), the average number of the player's Pokemon that faint, and the
clean rate (won with none fainting). Fights are ranked by the win rate
first and faints second; the clean rate is reported, not ranked on. One
fight in 25 moves a rate by four points, so differences of a few points
between readings are noise.

**What the numbers look like.** Readings on the simulator of 2026-10-03,
real odds, with the six the scorer chose:

| Fight | Won | Faints |
|---|---|---|
| Barry 2, cap 11 | 100% | 0.00 |
| Roark, cap 16 | 100% | 0.05 |
| Mars 1, cap 19 | 100% | 0.16 |
| Gardenia, cap 26 | 97% | 1.07 |
| Jupiter 1, cap 27 | 100% | 0.19 |
| Lucas and Dawn 2, cap 30 | 100% | 0.00 |
| Fantina, cap 33 | 91% | 3.04 |

Kaizo's own bosses of the same splits, read on the same boxes, are won 0 to
81% of the time (Barry 2 0%, Roark 81%, Gardenia 24%, Jupiter 80%,
Fantina 40%).

**What it does not yet model.** Double battles' AI partners; Gravity,
Foresight, Embargo and Judgment's plate; a two-to-five-hit move counts as
three hits; Baton Pass passes nothing; Camouflage and Secret Power's
secondary effect need the battle's terrain; Smack Down does not ground. The
learned judge misreads hard fights badly, so it only shortlists; every
number above comes from the full scorer.

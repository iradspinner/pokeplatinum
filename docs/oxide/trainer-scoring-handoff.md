# Trainer scoring: the handoff from the three-gym run

This is the brief for the agent that takes over training Oxide's trainer
scorer. On 2026-09-30 Ian and the Oxide Overseer played Roark, Mars 1 and
Gardenia by hand on the fight simulator, as a fresh three-gym run optimised
toward Fantina's cap of 33, to learn what a scorer must know before it can be
trusted. Every mistake along the way was a rule the simulator or the planner
did not have. This document collects those rules, the lines that won, the
simulator's state, and Ian's answers on how the work is to be run.

## The track

Ian gave this work to a new, dedicated session, the **Scoring Agent**
(2026-09-30). This document is its status home: it keeps a dated "Where it
stands" paragraph under this section and adds its findings below, the way the
balance plan does. Like every track it works on its own branch and the
Overseer lands it.

It owns the fight simulator, its trainer AI and the perfect-line scorer in
`tools/oxide/balance/` (Ian, 2026-09-30):

- `fightsim.py` and `fightai.py`
- `perfectline.py`, `perfectline.json` and `perfectline_results/`
- `plscore.py`, `plines.py`, `plkaizo.py`, `plrescore.py`, `plstep3.py`
  (step 3's runner, added 2026-10-01), `ppairs.py`, `pboxes.py` and
  `pdoubles.py`
- their tests: `test_fightsim.py`, `test_plfixes.py`, `test_pline.py` and
  `test_fightai.py` (the AI routine by routine, added 2026-10-01)

The rest of `tools/oxide/balance/` stays the balance track's. The balance
track runs the scorer for its passes and asks this track for any change to
it. The fightai audit, which the Balance Agent had paused, moves here with the
files.

**Ian checks this agent's reasoning** until he is reasonably sure it picks up
the trends the three-gym run found (2026-09-30). Until he says so, every fight
line the agent reaches, and every change to how the planner judges or
searches, goes to him with its reasoning before the agent builds on it. That
means the line turn by turn, the value behind each key choice, and which of
the nine ideas below arose on their own. A finding he has not checked stays a
draft. When the agent pauses for his check, it tells the Overseer first, in
one line.

**Starting the session.** Ian starts it with this prompt:

```
You are the Scoring Agent for Platinum Oxide. Read CLAUDE.md, then
docs/oxide/trainer-scoring-handoff.md, which is your brief and your status
home. Ian checks your reasoning on every line and every new planning idea
before you build on it. Start with step 1 of its order of work.
```

**Where it stands (2026-10-02).** The fightai audit and the known gaps are
on `oxide` (6ce38e1e26). The work now follows Ian's four goals in order ("The
order of work", below), on branch `scoring-step3-bar`: the scorer is rebuilt
as a planner (`plplan.py`) that decides turn by turn by simulating its options
at real odds (his rulings of 2026-10-01 and 2026-10-02, below). Its Roark
waits on Ian's check ("The planner's Roark, for Ian's check", below): 93%
clean against our 98.5%, every fight won, every loss to Lileep. Stage 1 of
the speed plan is closed (`docs/oxide/scorer-speed-plan.md`: the planner's
memory bounded after the WSL crash, the same fights move for move by
`plspeed.py`, PyPy no gain), and stage 2, a learned position value on the
GPU, has started at Ian's word. Every reading is now 75 fights at real odds
and 25 very unlucky. The perfect-line store has been stale since the simulator
fixes of 2026-09-30 (`test_pline` passes 1 of 3); its rescore, and the Kaizo
blind study before it, are entries in the tracker's Scheduled list. The
Kaizo reader's `perfectline_results/kaizo.json` was never committed; rerun
`plkaizo.py` rather than copying it.

## The job

The scorer's direction is already set in the balance plan
(`docs/oxide/balance-plan.md`, its opening section on the perfect-line
scorer). A fight reads as the clean-win rate of the best line found, with that
line's mean deaths and wipe chance beside it. Bosses are read with a planned
team, ordinary trainers blind. The boss target waits until the scorer reads
Roark sensibly. These three fights are the first bosses with hand-checked
answers.

Make the scorer find lines at least as good as the hand-played ones, on the
same box, by planning in the simulator rather than by rules written for these
fights (Ian, 2026-10-01). The nine planning ideas below are its exam: it must
rediscover each without being told. Then use it on the bosses.

The first acceptance check is the three fights below. A line is judged on
three numbers together, never the clean rate alone (Ian, 2026-10-01): the
clean rate (won with no Pokemon fainting), the win rate (won at all) and the
death count (the mean number of the player's Pokemon that faint per fight,
over every fight played). The death count is what separates the gnarliest
fights. The bar is our hand-played lines rerun on the corrected AI at real
odds (Ian, 2026-10-02), 2,000 runs each on seeds from the harness's own
start; the scorer's line must match or beat ours on the whole of the three,
and every report to Ian shows all three side by side, with the very unlucky
fight beside them.

| Fight | Our line | Dice | Clean | Won | Deaths per fight |
|---|---|---|---|---|---|
| Roark | S12 | real odds | 1970/2000 | 2000/2000 | 0.015 |
| Roark | S12 | very unlucky | 1928/2000 | 1999/2000 | 0.043 |
| Roark | S12 | old budget | 1979/2000 | 2000/2000 | 0.011 |
| Mars 1 | S1, the PP stall | real odds | 1927/2000 | 2000/2000 | 0.037 |
| Mars 1 | S1, the PP stall | very unlucky | 1825/2000 | 2000/2000 | 0.089 |
| Mars 1 | S1, the PP stall | old budget | 1929/2000 | 2000/2000 | 0.036 |
| Gardenia | L1 | real odds | 301/2000 | 1197/2000 | 3.212 |
| Gardenia | L1 | very unlucky | 96/2000 | 602/2000 | 4.680 |
| Gardenia | L1 | old budget | 296/2000 | 1188/2000 | 3.284 |

Each figure comes from the harness script's own `run()` (`compare3.py`,
`mars2.py` and `gardenia4.py` in `~/oxide-trials/three-gym-run/`), which plays
every fight to its end and returns whether it was won and how many of the
player's Pokemon fainted, with the variant each script's `main()` uses, on
seeds counting up from its own start (2000, 7000, 9000). The tally script
beside them, `three_numbers.py`, takes the run count and the dice. Two
thousand runs, rather than the 200 of the first bar, because a rare wipe of
about 2% shows only about four times in 200 runs, with a standard error near
one percentage point, and about forty times in 2,000. The old-budget rows
match the first bar of 200 runs (199, 191 and 29 clean) on their first 200
seeds. The figures before the audit (Roark 199, Mars 1 198, Gardenia 57
clean) were measured on an AI that got many picks wrong, and no longer
count.

Beating our Gardenia line is welcome. Our planning there was not optimal: the
run that lost Vikavolt had a better play at turn 12 than our rules found
(Popplio takes the Rock Tomb and Icy Winds Shiftry out).

## The ground truth

The box was rolled area by area, as the run would meet it:

- **Encounter rules:** dupes re-rolled, one capture per location name, and
  honey trees counted (Ian).
- **Trades:** Charap's Popplio was taken for Finneon, and Kazza's Vullaby
  (nicknamed Kazza) for Blipbug.
- **Items:** only those the item census places before each fight. TMs are left
  out until the TM pass.
- **Evolutions:** held where a level-up move came earlier in the line:
  - Charmander to 25 for Fire Fang
  - Mareep to 28 for Discharge
  - Popplio to 31 for Scald
  - Grubbin one level, to 21, for Spark

The full box is in the harness README.

| Fight | Cap | Team | Line in brief | Clean wins | Played |
|---|---|---|---|---|---|
| Roark | 16 | Barboach, Steenee, Nidorino, Onix, Geodude (Quick Claw), Prinplup | Barboach Mud Bombs Nosepass. Steenee takes Lileep's Mega Drain and Play Nices it, and Nidorino finishes it. Barboach comes in on Geodude's Thunder Punch and Onix finishes Geodude. Onix Screeches and Rock Throws Cranidos | 199/200 | seed 30, clean |
| Mars 1 | 22 (soft) | Geodude (Quick Claw), Kazza, Starly (level 6), Onix, Charjabug, Nidorino | Geodude knocks out Meowth, so Bronzor comes in on it. Kazza and Starly trade places until Bronzor has no Confusion left. Bronzor struggles and Pluck finishes it. Pluck takes Zubat, and Onix takes Purugly | 198/200 | seed 31, clean |
| Gardenia | 26 | Charmeleon, Popplio, Vikavolt, Kazza, Golbat (Quick Claw), Tsareena | Charmeleon takes Cherrim. Popplio Sings Lumineon, and Vikavolt Sparks it out after the sun. Kazza's Pluck takes Shiftry's Occa Berry, so it charges Solar Beam, and Golbat walks in on the charge. Golbat outspeeds Breloom and Roserade out of sun | 57/200 | seed 32, won losing Vikavolt |

Gardenia is the hard one. The finale (Golbat at full HP against Roserade, out
of sun) wins 94%. Everything before it has to keep Golbat untouched and outlast
the sun. The losses split between the Lumineon stage (Swagger, Silver Wind and
Natural Gift wearing down the Singer) and the Shiftry stage (a pivot that takes
one Solar Beam falls into Rock Tomb's knockout range, so Shiftry picks Rock Tomb
over the charge). Ian reads the 28% as mostly the box's (2026-09-30): the
player's move pools look sparse in interesting options and lack many of the
more interesting modern moves, so they are the first thing to change, not
Gardenia's team.

## What a scorer must model

### The trainer AI, exactly

Read every rule from `docs/oxide/battle-ai/` and the decomp
(`src/battle/trainer_ai/`), not from memory or a general guide. Each of these
decided a fight:

- A speed tie counts as not slower in the speed-lowering routines. So Lileep's
  Rock Tomb scores -3 against a Pokemon at its speed, and it uses Ingrain
  instead. That gave free turns at Roark.
- Evaluate Attack costs moves at their listed power (Rollout at 30), and its
  knockout check uses Pursuit's undoubled damage.
- A knockout bonus makes the AI pick whatever move knocks out the target. That
  is why Breloom picks Rock Tomb against anything in its range, and why Shiftry
  picks Rock Tomb over Solar Beam against a weakened pivot.
- Basic's checks change picks in four ways:
  - Status moves skip the type-immunity check, so Hypnosis is aimed at a Dark
    type.
  - Powder moves score -10 against Grass types (Oxide).
  - Swagger scores -5 into a target that is already confused.
  - Natural Gift fails without a berry.
- `BattleAI_PostKOSwitchIn` picks the next Pokemon against whoever made the
  knockout, so knockout ownership is the player's main lever. The harness
  prints the full map for each fight.
- `TrainerAI_ShouldSwitch`, as the decomp has it, with its randomness. Three
  points differ from pokemow's page:
  - The super-effective gate holds only nine times in ten per move.
  - The party checks are 50% (immune) and 33% (resisting) per move.
  - In singles, each move is rolled twice in the all-immune check.
- The AI types variable moves the way the battle does. Weather Ball takes the
  weather's type. Natural Gift takes its berry's type (from
  `res/items/data/<berry>.json`), so Lumineon's Watmel gift counts as Fire.

### Mechanics that decided turns

- **Oxide forces the Set battle style.** A switch always costs the incoming
  Pokemon a hit, except after one of the player's own faints, when the
  replacement comes in free.
- **Weather is a clock.** Sunny Day has 1 PP, and a Heat Rock gives 8 turns.
  Chlorophyll doubles speed only while the sun lasts. Solar Beam needs a charge
  turn outside the sun.
- **PP is a resource.** Calm Mind has 3 PP in Oxide. With every move empty, a
  Pokemon struggles and loses a quarter of its HP each time.
- **Items:**
  - Berries matter: Sitrus, Apicot, Occa, Watmel.
  - Pluck and Bug Bite eat a berry, and Knock Off removes any item.
  - Big Root makes Ingrain and Mega Drain heal more.
  - Quick Claw moves its holder first one time in five.
- **Abilities in play:**
  - Flash Fire absorbs Weather Ball in sun.
  - Simple doubles Swagger's boost to +4, which doubles the self-hit too.
  - Leaf Guard blocks status in sun. The engine knows this; the AI does not.
  - Natural Cure makes a sleeping holder switch out often.
  - Also in play: Technician, Sturdy, Solid Rock and Battery.
- **Critical hits** are 1 in 24 at 1.5 times. They ignore attack drops and
  screens, but not burn. A second Play Nice is only safe after the fight's crit
  has landed.
- **Confusion** hits its holder half the time (`RandNext & 1`), using its
  boosted Attack.

### Luck: real odds, and a very unlucky fight (Ian, 2026-10-02)

Ian retired the luck budget from measurement on 2026-10-02. Every fight is
simulated at the game's real odds: a secondary status against the player
lands at its chance, crits land 1 in 24 with no cap on how many, and ties
between equal AI picks break at random as before. The three numbers are then
true frequencies with bad luck already inside them. His reason: under the
budget every run assumed Sludge Bomb poisons, which never happens, while two
crits, which land in about one long fight in five, were ruled out, so Wake
and Cynthia would read easier than they play. The planner's caution comes
from its position value: a faint costs heavily, so it avoids a play with a
real chance of a chain into a faint, at that play's true odds, with each
chance in its look-ahead weighed exactly where it can be.

Beside the real-odds numbers, each line is replayed as a very unlucky fight,
the stress test. Every status check and every crit check, the trainer's and
the player's alike, rolls twice and keeps the result worse for the player:
the trainer's crit lands about 1 in 12, a 10% secondary status on the player
about 19%, and the player's own crits and secondary effects need both rolls.
The player's full-paralysis and confusion self-hit checks also take the
worse roll. Damage rolls and accuracy stay at the game's odds. Ian suspects
disadvantage on both sides may be too harsh: if the stress readings stop
telling lines apart (most lines near zero clean, or their order collapsing),
the numbers go to him first, with the same lines under disadvantage on the
trainer's checks only, so he can choose. His first targets for an ordinary
trainer and a gauntlet were set under the budget, so they are provisional
until his first run's ratings recalibrate them.

The old budget, for the record (2026-09-30 to 2026-10-01): every secondary
status against the player landed, at most one crit landed on the player,
and plans were built to survive that crit at its worst moment, which is why
our Steenee hands over after one Play Nice. `perfectline.LUCK` keeps all
three settings ("real", the default; "unlucky"; "budget"), so the old bar
can be re-measured.

### The planning ideas that won fights

These are the scorer's exam (Ian, 2026-10-01). A planner that simulates its
options forward and values the position it reaches must rediscover each one
in the three fights without being told. When it misses one, the fix goes into
the general machinery (how far it looks, what the position's value counts),
never into a behaviour named for the idea. A one-turn heuristic does not find
them.

1. **Bait by knockout ownership.** Choose who makes each knockout so the
   trainer's next Pokemon meets an answer. This decided Roark and the Gardenia
   line.
2. **Free switch on a predictable pick.** Bring a Pokemon in on a turn whose
   move is known to be harmless to it:
   - Ingrain on a speed tie (Roark)
   - Mega Drain at a four-times-weak target, taken by a resister
   - a berry-less Shiftry's Solar Beam charge (Gardenia)
   - Bronzor's moves into a Dark type (Mars)
3. **PP stall.** An immune pivot and a fodder in knockout range trade places,
   so every damaging move is spent on the immune one (Mars, Ian's trick).
4. **Run out a timed effect.** Spend the sun's turns on a foe that cannot hurt
   much, or on one asleep.
5. **Remove a key item.** Take Shiftry's Occa Berry with Pluck so Natural Gift
   fails and its pick becomes predictable.
6. **Control speed and status.** Play Nice never misses. Also used: Screech,
   Sing, Rock Tomb and Will-O-Wisp.
7. **Exploit coverage holes.** Bronzor's only attack is Psychic, so a Dark type
   stops it (Ian's hint for Mars).
8. **Sacrifice for tempo.** Lose the box member that scales worst (here
   Bibarel, never a super-wanted line) to get a free entry where it matters
   most (Ian's idea for Gardenia). In our runs it added wins but no clean ones.
9. **Build the box for the fight and beyond.** Hold an evolution for a move.
   Keep a deliberately low-level fodder (Starly at 6). Take a trade for a
   missing type (Kazza's Vullaby).

## What did not work

Generic rules make player mistakes. Examples from the traces:

- leaving a sleeping, half-dead foe because the attacker was confused
- switching a Pokemon to itself
- sending a Flying type into Rock Tomb's knockout range
- a sleeping Pokemon switching out, which gives the foe free turns while the
  sleep counter does not tick

A look-ahead player that tries every option and rolls the fight forward with
fresh dice did no better than the plan it rolled forward with. Its estimates
were too noisy, with clean wins as the only reward. It even left a certain
Fire Fang line at Cherrim.

Walls that soak Lumineon through the sun bled out under Swagger. Ian's
Dubwool and Charmeleon pivot lost Charmeleon to Aqua Tail in about a
third of runs. When Dubwool made the knockout, the order also changed to Breloom
before Shiftry, which our later stages were not built for.

The lesson first drawn here was that the scorer needs the planning ideas as
moves in its search. Ian ruled against that on 2026-10-01 ("Ian's ruling on
step 3", below). The look-ahead failed for two reasons a planner can avoid:
it scored only clean wins, so nearly every rollout said the same thing, and
it looked one decision ahead.

## The simulator

The fixes from this work are on `oxide` since 153d11de2, with tests in
`tools/oxide/balance/test_plfixes.py` (24 of 24) and `test_fightsim.py`
(17 of 17). The last five were:

| Commit | Fix |
|---|---|
| 0501036640 | Only Thunder Wave among status moves meets the type chart, in the engine and the AI |
| 435f72e6ce | Struggle when no move has PP |
| bbbe4b72a9 | The player's Quick Claw fires (it never did) |
| 095fe2f58c | Powder immunity for Grass types and Overcoat, in the engine and the AI; Leaf Guard in the engine |
| 48ed15ab6b | The switching rules as `TrainerAI_ShouldSwitch` has them, and real types for Weather Ball and Natural Gift |

Earlier fixes:

- Magnitude rolls its power.
- Rollout's power is fixed.
- The AI's speed-lowering, Pursuit and Defense Curl routines are corrected.
- Block's trap and Ingrain are tracked.
- Pinch berries fire.
- `BattleAI_PostKOSwitchIn`'s second stage is fixed.

The known gaps of 2026-09-30 are closed on `scoring-fightai-audit`
(2026-10-01):

- **Fixed-damage moves** take their scripts' figures, untouched by stages,
  screens or critical hits, and do nothing to an immune type; one-hit KO
  moves fail into Sturdy. Ian's ruling that Charmander has no Dragon Rage in
  Roark's split is still held for the next learnset revision.
- **The move that last hit** is recorded as the engine records it: any move
  aimed at the Pokemon, status moves and misses included.
- **Oxide's Phase 4 AI catch-up rules** are all in, through the audit below.
- **Sleep length** matches the engine (a counter of 2 to 5, one off per move
  attempt); Early Bird, which was missing, takes two off.

## The fightai audit (2026-09-30 to 2026-10-01)

Four read-only audits compared the port with `script.s` and `trainer_ai.c`
at HEAD, one each for the score engine with Basic and Evaluate Attack, the
two halves of Expert, and the smaller flags with switching. The Scoring
Agent checked each headline claim against the script before applying it, and
settled the points where the audits disagreed by reading the engine. Each
routine has a check in `test_fightai.py`, pinned with every chance passing
and every chance failing; most of those checks fail on the old port.

What the old port got wrong, in the rules that decide fights most:

- Expert ran a condensed list. 62 of its routines scored nothing, among them
  Curse, Sleep Talk, Baton Pass, Destiny Bond, Counter, Mirror Coat, Bug Bite
  and the charge-turn moves; seven names in its sets were not effects at all,
  so Quiver Dance, Shell Smash, Coil, Work Up and Hone Claws scored nothing.
  Expert now reads its jump table from the script, one routine per label.
- Evaluate Attack never reached its -2 for Sucker Punch, Explosion and Focus
  Punch, and gave the knockout +6 by priority instead of by effect.
- The damage figure counted every hit of a multi-hit move, included Life
  Orb, and left out Low Kick, Hidden Power, Natural Gift and the other moves
  listed at power 1.
- The AI read the player's real ability; the game guesses between the
  species' two regular abilities until a battle message names one.
- Check HP had two bands where the script has five tables; the Baton Pass
  flag had no routine; Risky and Harassment had the wrong lists.
- The switch rules ran after a Choice lock instead of before it, missed
  Shadow Tag, Arena Trap and Magnet Pull, and read effectiveness as a type
  product where the engine reads chart flags (Levitate counts, and an
  immunity met first does not stop a later weakness).
- The post-knockout pick took a candidate with a type score of 0, and costed
  moves without the target's stat stages; the engine's never-reset score is
  now kept.
- Tag Strategy ran only in doubles and only lightly; the partner pass did
  not exist, so Belle and Pa's Ninetales never aimed Flamethrower at its Flash
  Fire Vulpix as the game does.

Two engine facts the brief did not have. The AI knows the turn's Quick Claw
roll: `speedRand` is rolled before the AI chooses and read again by the turn
order, so on a turn the player's Quick Claw fires the AI reads itself
slower; in a run the simulator now draws the roll first. And the calculator's
rows already cap damage at a Sturdy target's full HP less one, so against
Sturdy every strong move ties in the AI's figure where the engine has one
strongest (recorded, not fixed).

The simulator gained, beside the gaps above: Explosion fainting its user
before the hit (into a Ghost or Protect too, Damp aside), the turn count of a
Pokemon switched in mid-turn (Fake Out no longer works on a lead's second
turn), the previous move cleared on a turn the Pokemon could not act, Speed
in whole numbers with Quick Feet, Hyper Cutter, Keen Eye and Big Pecks
stopping drops, Brick Break and Infiltrator passing screens, Flash Fire lit
by a Fire move (and its boost taken off while unlit), Sleep Talk and Aqua
Ring, and the abilities a battle message names. The perfect-line search's AI
cache key now covers everything the AI reads, and the search no longer
offers a trapped player a switch.

The three hand-played lines, rerun on the same seeds:

| Fight | Line | Before the audit | After |
|---|---|---|---|
| Roark | S12 | 197/200 | 199/200 |
| Mars 1 | S1, the PP stall | 198/200 | 191/200 |
| Gardenia | L1 | 57/200 | 29/200 |

Mars 1 changes through the post-knockout pick. After Geodude knocks out
Meowth, Bronzor came in every time; it still does when Geodude's Defense is
unchanged, since Confusion against its low Special Defense outscores every
physical move. But Meowth carries Screech, and in runs where it has Screeched
Geodude to -2 Defense, Zubat's Bite (first in party order) outscores
Confusion and Zubat comes in. "Geodude knocks out Meowth, so Bronzor comes
in" holds only when Meowth has not Screeched first.

Gardenia changes through her picks, each a rule the game has. Solar Beam
into a target that resists it takes -2 (Golbat, Vullaby, Tsareena) and in
sun into Popplio +2. Breloom's and Roserade's Stun Spore into Vullaby is
refused half the time (the AI guesses Overcoat), and Breloom's Mach Punch
into Tsareena half the time (Queenly Majesty). Bullet Seed no longer reads as
Breloom's strongest attack. Natural Gift now has its berry's figure:
Shiftry's becomes certain against Tsareena and Vikavolt, and Lumineon's is
used when it is strongest, mostly in sun. The Golbat and Roserade finale
alone is unchanged (279 of 300 at full HP); Golbat now reaches it hurt more
often.

Left open, none changing a pick in a fight Oxide has now: the AI partners
beside the player and the switch rules in double battles were not ported;
Me First and Copycat need calculator rows of a Pokemon on itself; Judgment's
plate, Gravity, Magnet Rise, Foresight, Embargo and genders are not
simulated, so the routines reading them stay off; in the strict search a
trainer's Quick Claw is still a luck event its AI does not foresee, and
Sleep Talk calls the first eligible move; the damage model counts a
two-to-five-hit move as three hits.

## Ian's answers on the audit (2026-10-01)

1. **The bar for step 3:** our hand-played lines rerun on the corrected AI,
   not the old figures, judged on the clean rate, the win rate and the death
   count together. The table under "The job" holds all three for each line.
2. **The rescore:** not yet. Once step 3 passes Ian's check, the Scoring
   Agent's learnings and the scoring method go to the Kaizo blind study,
   which gives a broad comb to shape Oxide's trainers quickly; the full
   rescore of the 459 fights comes after that comb. Both wait in the
   tracker's Scheduled list.

## Step 3, the first reading (2026-10-01)

This is a draft until Ian has checked it. The scorer's line search
(`plines.py` at the planned budget: 300 candidate lines, each screened on 20
runs, the best three confirmed on 300) read each fight two ways. With our six
and our held items, four independent searches ran, so a shortfall is the
search's own. With the run's whole box at the fight (16 Pokemon at Roark, 20
at Mars 1, 23 at Gardenia), the scorer chose its eight planned sixes and held
items by its own rule from the run's stock. Each reading's best line was then
replayed on the harness's 200 seeds and judged on Ian's three numbers. The
runner is `tools/oxide/balance/plstep3.py`; the readings, a trace of each best
line on the hand line's showcase seed, and a tally of where each line loses
Pokemon are in `tools/oxide/balance/perfectline_results/step3/`. The tally
script that reproduces the bar is `~/oxide-trials/three-gym-run/three_numbers.py`,
and it gave the table under "The job" exactly.

| Fight | Line | Clean | Won | Deaths per fight |
|---|---|---|---|---|
| Roark | ours | 199 | 200 | 0.005 |
| Roark | search, our six | 56 | 199 | 1.155 |
| Roark | search, whole box | 27 | 100 | 3.590 |
| Mars 1 | ours | 191 | 200 | 0.045 |
| Mars 1 | search, our six | 198 | 200 | 0.010 |
| Mars 1 | search, whole box | 197 | 200 | 0.020 |
| Gardenia | ours | 29 | 116 | 3.325 |
| Gardenia | search, our six | 12 | 42 | 5.110 |
| Gardenia | search, whole box | 3 | 58 | 4.975 |

**Mars 1 passes.** With our six, Starly leads and switches to Nidorino on
turn one, so Nidorino takes the Fake Out Meowth aimed at Starly. Nidorino's
Double Kick knocks Meowth out and Bronzor comes in. Vullaby comes in on it and
Plucks it down over about twenty turns: on the corrected AI Bronzor never aims
Confusion at a Dark type, so it spends its turns on Calm Mind, Hypnosis and
Confuse Ray. Vullaby then takes Zubat, ending near a fifth of its HP, and
Onix's Rock Tomb takes Purugly. It used ideas 7 (Bronzor's coverage hole) and
2 (Nidorino takes a hit chosen against Starly). It did not need the PP stall
(idea 3), which answered picks the old AI made. The whole-box line reaches
the same answer with Onix, Bibarel and Vullaby, but plays one stretch badly:
Bibarel keeps choosing Defense Curl while asleep and falls to 3 HP before
Onix returns. The three numbers do not show that.

**Roark falls short.** With our six, the first death is Steenee to Lileep in
136 of 200 runs. The search reads each exchange without the foe's healing, so
it scores Steenee as beating Lileep and gives Lileep a single answer rather
than a hand-off. Steenee stays in after its Play Nice until it faints, and
Prinplup cannot then outpace Ingrain and Mega Drain. Our line hands Steenee
over to Nidorino after one Play Nice, at a HP that survives a crit. Two
smaller gaps: Onix spends its first turns on Harden while Nosepass Blocks and
lays Stealth Rock, and Onix never Screeches Cranidos (39 of Onix's deaths),
since the line's stat-drop rule lowers only an attacking stat or accuracy.
From the whole box the six-picking reads Lileep the same way and leaves
Steenee out, and Lileep takes Nidorino first in 110 runs.

**Gardenia falls short.** The search sets its answers from the opening state,
before the sun, so it sends Tsareena into Cherrim's Weather Ball in sun (77 HP
to 7 in one hit) and Vikavolt into Lumineon's sun turns. The first deaths are
Vikavolt to Lumineon (69 runs), Golbat to Shiftry (49) and Tsareena to
Cherrim (45). None of the line's rules can play our line's ideas. Its sleep
rule aims only at the foe's strongest Pokemon, so Popplio never Sings
Lumineon. Its stall rule waits out screens, Tailwind and Trick Room but not
the sun (idea 4). Nothing removes Shiftry's Occa Berry (idea 5). Its free
pivot only leaves a losing exchange, so Golbat never walks in on a
predictable Solar Beam charge (idea 2).

**Withdrawn: the proposed rules.** This reading proposed three new rules for
Roark (the foe's healing read into who wins an exchange, a hand-off after one
stat drop, and Screech) and four for Gardenia (answers read in the sun, sleep
on any foe, taking a berry, a switch-in on a charge turn). Ian ruled none of
them is built ("Ian's ruling on step 3", below). They stay here as a record
of what the rule-based search missed, which the planner must find on its own.

**Notes on the reading.**

- The item census counts a Hard Stone on the third floor of Oreburgh's
  northwest house, which pret marks unused, so a player most likely cannot
  reach it. The box readings use the run's own stock instead (Flame Plate;
  then Miracle Seed; then Draco Plate). The census is the balance track's to
  check.
- The scorer's item rule never hands out a Quick Claw, so the whole-box lines
  play without one; the our-six lines hold ours.
- The bar plays the harness's turn order, where the trainer's AI never sees
  the player's Quick Claw roll. The scorer plays the engine's order, where it
  does. The two differ only on turns Geodude's or Golbat's Quick Claw fires.
- The harness has no moves for eight of the box's Pokemon (Corvisquire,
  Finneon, Charmander, Mareep, Graveler, Breloom, Snover, and Krabby after
  Roark), nor for Wooloo, Vulpix, Steenee and Skiploom at Mars 1. Theirs are their level-up moves
  alone, from the run's catch levels through its evolutions and holds, as
  `plstep3.py` lists.

## Ian's ruling on step 3 (2026-10-01)

Ian read the first reading of Roark, where the search missed Lileep's
healing, the hand-off after one Play Nice and Onix's Screech. His words:

> We need the scorer to be able to adapt to things, otherwise we will have
> to programatically include every team possibility ever... need to then
> organically arise otherwise this is a doomed project.

So no rule named for a plan is added to the search, and the order of work's
old instruction (find which planning idea the search lacked and add it as a
move) is withdrawn. The nine planning ideas become the scorer's exam.

The direction he approved, relayed by the Overseer:

- The scorer becomes a planner that decides turn by turn, replacements after
  a faint included, by simulating its options forward in the real simulator.
- The trainer's AI is known exactly, so the planner computes the AI's choice
  distribution at each turn from the AI itself rather than sampling it. The
  only other uncertainty is the dice, under Ian's luck budget: every
  secondary status against the player lands, one crit against the player may
  land at its worst moment and never two, and ties between equal AI picks
  break at random.
- A position is valued by its state, not only by the fight's result: each of
  the player's Pokemon's HP and whether it survives (a faint costs heavily,
  since every loss narrows later team-building), the foe's HP, items, the
  weather's turns left, PP, stat stages and status. Long-range plays (taking
  Shiftry's Occa Berry, waiting out the sun) may appear through how far the
  planner looks or what the value counts, since those describe the position.
- Choosing a six from the whole box uses the same planner as its judge.
- The computing cost per fight is measured and reported, since the rescore
  of 459 fights depends on it.

What Ian checks first: the planner's play of Roark, turn by turn on a
showcase seed, the value behind each key choice, which of the nine ideas
arose on their own and which did not, and the three numbers beside ours
(199, 200, 0.005) and the rule-based search's (56, 199, 1.155). Nothing
further is built until he has checked it.

## The planner's Roark, for Ian's check (2026-10-02)

This is a draft until Ian has checked it. The planner (`plplan.py`) played
Roark with our hand-played six and items (Barboach, Nidorino, Geodude with the
Quick Claw, Onix, Prinplup, Steenee, all at 16). It falls a little short of
our line: about 93% clean against our 98.5%, every fight won, and every Pokemon
it lost fell to Lileep.

**The numbers.** Each line was played to the end of the fight many times on
seeds counting up from 2000. "Clean" is the share won with no Pokemon
fainting, "won" the share won at all, and "faints" the average number of the
player's Pokemon that fainted per fight. "Real odds" is the game's own luck.
"Very unlucky" rolls every status and crit check twice and keeps the result
worse for the player. The planner's rows are Ian's reading size, 75 and 25
fights (2026-10-02); ours and the rule-based search's are over 2,000.

| Line | Dice | Clean | Won | Faints |
|---|---|---|---|---|
| Ours (the hand-played S12) | real odds | 98.5% | 100% | 0.015 |
| The planner | real odds | 93.3% (70 of 75) | 100% | 0.067 |
| The rule-based search, searched at real odds | real odds | 32.7% | 85.3% | 1.607 |
| Ours | very unlucky | 96.4% | 99.95% | 0.043 |
| The planner | very unlucky | 84% (21 of 25) | 100% | 0.160 |
| The rule-based search | very unlucky | 28.2% | 82.6% | 1.760 |

Under the old budget, which no longer counts, ours read 199 of 200 clean and
the rule-based search 56. The planner's five faints at real odds were all to
Lileep: Nidorino three times, Steenee and Prinplup once each. With 75 fights
a clean rate of 93% carries a standard error of about three points, so the
gap to ours is real but small.

**How it chooses.** Before each turn the planner lists its options (every
move that would do something, every switch) and works out the trainer's
choice exactly from the AI's own code. It weighs every chance in the coming
turn at its real odds, then plays the fight on from each position the turn
can reach and averages how those fights end. A position's value is minus one
for each faint, minus ten more for a lost fight, plus a tenth of each
survivor's share of HP at the end. So +0.43 is a clean win with most HP left,
and -0.7 is roughly a faint to come. An option that is clearly behind is
dropped after a few play-outs, and the close ones get the full count.

**The line on the showcase seed (30)**, which it won cleanly
(`perfectline_results/step3/planner-roark-trace-seed30.txt` has every turn):

1. Geodude leads into Nosepass, sets up Rock Polish while Nosepass Blocks, and
   Magnitudes and Rock Throws it down.
2. Lileep comes in on Geodude, which is four times weak to Grass. The planner
   switches to Steenee (-0.71) rather than staying in (about -0.85) or sending
   Prinplup (-0.75). Steenee takes the Mega Drain resisted.
3. Steenee uses Play Nice (-0.67) rather than Razor Leaf (-0.82): lowering
   Lileep's Attack is worth more than Steenee's own damage.
4. At 21 of 45 HP Steenee hands over to Nidorino (+0.24, against -0.54 to
   -0.74 for everything else): Nidorino beats an Attack-lowered Lileep, while
   Steenee staying in risks a faint. Nidorino's Double Kick and Poison Sting
   finish Lileep.
5. Roark's Geodude comes in on Nidorino. The planner brings Barboach in on the
   Thunder Punch it expects (+0.28, against -0.15 at best otherwise), which
   cannot touch a Ground type, and Mud Bombs it low.
6. Onix comes in, finishes Geodude, Screeches Cranidos (+0.43) and Rock
   Throws it out in three.

That is nearly our own line. We led Barboach into Nosepass where it leads
Geodude; the Lileep and Cranidos stages match.

**The nine ideas, as an exam.** Arose on its own: the free switch on a
predictable pick (Steenee on Mega Drain, Barboach on Thunder Punch), speed and
status control (Play Nice, Screech), and the coverage hole (a Ground type
against Thunder Punch). The hand-off after one Play Nice, at an HP that
survives the next hit, also arose. Not seen: bait by knockout ownership. The
planner never arranged who made a knockout so that the next foe met an
answer; it switched to the answer afterwards instead. Did not apply at Roark:
the PP stall, running out a timed effect, taking an item, a sacrifice, and
building the box (our six was given).

**What it still does badly.** When several options read within a hundredth of
each other, it picks among them almost at random. So it wastes turns: Rock
Polish on turn one, Defense Curl against a Nosepass on 3 HP, Bind and three
Hardens against a Geodude on 2 to 6 HP. It got away with it here, but each
wasted turn is another turn of the foe's luck, and Rollout grows meanwhile.
Its Lileep losses come from the same root: the play-outs that value a position
are played by a plain policy that judges Lileep poorly, and a single play-out
is noisy. Stage 2's learned value is the general machinery that should help
both, since it replaces those play-outs with a smoother estimate.

**Cost.** About 113 seconds of one core per fight and 24 decisions, so the 75
fights took 342 seconds on 29 workers (about 790 fights an hour). Each worker
holds at most about 190 MB.

## The harness

The working scripts are in `~/oxide-trials/three-gym-run/`, with a README:

- the rolled box
- each fight's damage table, replacement map and AI-pick probes
- each plan as rules
- the look-ahead player

They are notes for one box and one fight each, not tools. They show how each
answer above was found and give a way to re-check it. Run them from a checkout
of `oxide` at 153d11de2 or later.

## The order of work

Steps 1 and 2 are done: the fightai audit against the battle-ai docs and the
decomp, with a test per routine, and the known gaps filled (both on `oxide`
at 6ce38e1e26). Ian set the goals from here in order (2026-10-02); the speed
plan (`docs/oxide/scorer-speed-plan.md`) holds how the planner is made fast
enough for the last of them.

1. **Roark, relatively quickly, passing its tests.** The planner plays our
   six and must meet the bar on the three numbers at real odds (the table
   under "The job"), and Ian checks its reasoning: the line turn by turn, the
   value behind each key choice, and which of the nine ideas arose on their
   own. Where it falls short, the fix goes into its general machinery (how far
   it looks, how it values a position, how it reads the AI), never into a
   behaviour named for an idea. Stage 1 of the speed plan, which may not
   change any answer, serves this step.
2. **The three-gym split, through Fantina at cap 33,** under the three-gym
   run's rules: the box rolled area by area, one capture per location name,
   dupes re-rolled, honey trees counted, the two trades, only the items
   reachable by each fight, TMs out until the TM pass, and evolutions held for
   moves. Every major fight must pass. Roark, Mars 1 and Gardenia are held to
   their hand-played bars. The fights with no hand-played bar (the rival
   fights, Jupiter 1 and Fantina) pass when Ian has read the scorer's line and
   reasoning for each and accepts it; he chose that over hand-playing them
   first, so the earlier step of playing the next bosses with him by hand is
   gone. The Kaizo study's broad comb of the trainers comes after this step.
3. **Every major boss, rival, named Galactic fight and Ace Trainer,** on the
   combed teams, each boss over a spread of boxes (Ian's answer 3 below).
4. **Everything, the full rescore,** in a matter of hours with the spread of
   boxes and the stress test included: the speed plan's goal.

## Ian's answers (2026-09-30)

1. **Who takes this on:** a new, dedicated agent, the Scoring Agent ("The
   track", above). Ian checks its reasoning until he is sure it picks up the
   trends found here.
2. **Wins that lose a Pokemon.** The goal is to beat the game, so a win that
   loses a Pokemon is still a win and the run goes on. But each loss takes
   options away from the player's later team-building, so a player generally
   plays not to lose any. The scorer keeps the clean-win rate as its
   headline. It reports wins with losses beside it, along with what was
   lost, and a planned sacrifice counts as a cost, not as a failure.
3. **The box model for bosses:** a spread of boxes. The point is that a
   fight's answers must not narrow to one Pokemon. Read each boss over many
   rolled boxes, and report how the best lines spread across them. Flag a
   boss whose winning lines all lean on the same Pokemon.
4. **What Gardenia's 28% means.** Ian's first candidate for change is the
   player's move pools, not her team. They look sparse in interesting options
   and lack many of the more interesting modern moves. This goes to the
   balance track's learnset work, not to this track.
5. **AI ties:** break at random, as the simulator does now.

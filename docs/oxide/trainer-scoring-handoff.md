# Trainer scoring: the handoff from the three-gym run

## Summary for Ian (kept current with every commit; last 2026-10-06)

**Outcome.** The scorer reads a fight by playing it turn by turn in the
simulator at the game's real odds, 100 fights a reading (75 at real odds,
25 very unlucky), and reports how often it is won, how many Pokemon faint
and how often it is won with none fainting. A boss gets a six the team
search chooses from the box; an ordinary trainer gets a random six from the
box's stronger half. Goals 1 and 2 (Roark's split, then the run through
Fantina at 33) are passed. On 2026-10-06 the Kaizo study's comb of Roark's
split was read (one of eighteen checks passed; you approved the comb as
built), learnset checks 2 and 3 went to the balance track, and the change
to Poison Fang left no reading stale.

**Your action items.** None today. When you want double and tag battles
read (about 60 fights after Roark's split), say when; the estimate is
below.

**Next steps, and how long each takes on this machine.** The study's
exports are done (`goal3.csv`, the boxes after Fantina's split, the blind
pools at 19 to 33, in `~/oxide-trials/kaizo-teams/`). Goal 3 waits until the
learnset rewrite and the TM pass have landed, since both change the
player's box; it then runs once, on the comb's teams as far as the comb has
got, for the comb, step 5's boss bands and the alpha's boss order (Ian,
2026-10-06; the tracker's Scheduled list). Until then nothing is queued but
step 5's boss bands, when the balance track reaches them.

| Step | Takes |
|---|---|
| Goal 3, once: the bosses by the team search | about 1 to 2 hours a boss; about 22 hours for all 39, or 15 with one set of labels a boss |
| Goal 3's ordinary trainers, read blind | 5 to 30 minutes each, several at once |
| Double and tag battles, on the backlog: build and check the planner for them | about 3 to 4 working sessions, then your check of one hand-played double |
| Then reading the 60 or so doubles | roughly 60 to 100 hours of machine time, if a double costs 2 to 3 times a single |

The rest of this document is the track's working record. The latest
readings are in its sections dated 2026-10-03 and 2026-10-06, from "Goal 2's
readings" to "Learnset checks 2 and 3".

## The brief

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

**Where it stands (2026-10-03).** The fightai audit and the known gaps are
on `oxide` (6ce38e1e26). The work now follows Ian's four goals in order ("The
order of work", below), on branch `scoring-step3-bar`: the scorer is rebuilt
as a planner (`plplan.py`) that decides turn by turn by simulating its options
at real odds (his rulings of 2026-10-01 and 2026-10-02, below). Stage 1 of
the speed plan is closed (`docs/oxide/scorer-speed-plan.md`), and stage 2's
networks, learned from the play-out planner's own values, choose for it at
about a fortieth of the cost. **Goal 1 is passed** (Ian, 2026-10-02, "close
enough, pass"): the average of three networks (d1b+d2+d3) reads Roark at
97.7% clean, 100% won, 0.025 faints over 2,000 fights, against our line's
98.5%, 100%, 0.015 ("The network planner's Roark, for Ian's check"). It also
meets the Mars 1 bar, and Ian passed its Gardenia line as good enough for
now. The planner ranks its options by Ian's order, wins first and faints
second ("Wins first, then faints"). Goal 2 has begun: the rival fights of
Roark's split are read (Barry 1 is ruled not to count), and goal 2's boxes
are built from Ian's accepted choices. A network judges easy trainers it
never saw nearly as well as play-outs, but not a held-out boss or Ace
Trainer, so goal 3's fights each need labels of their own ("The cost of
labelling every boss"). For bosses the scorer now chooses its own six: the
team search, with its two fixes, found our six's equal at Roark and sixes
better than ours at Mars 1 at 19 and Gardenia ("The team search's first
test"), and it now ends with Ian's diagnose-and-loop. The learned stand-in
player failed its test, and budget 64 chooses as well as 192 ("The learned
stand-in player, and smaller budgets"). Goal 2's four fights with no
hand-played line are read, on a simulator that now has Magnet Rise,
Torment, Pain Split and Destiny Bond ("Moves the simulator ignored"):
Barry 2, Jupiter 1 and Lucas and Dawn 2 are easy, and Fantina is won about
19 times in 20 at two or three faints ("Goal 2's readings"). **Goal 2 is
passed** (Ian, 2026-10-03, "Ian's answers (2026-10-03)"): play-out readings
now run at budget 64 with a five-point tolerance on wins, and the loop
stands as built. Since then genders, Attract and Cute Charm, Wish, Spite
and Recycle, and two sweeps of battle-state items, abilities and move
effects are in ("Moves the simulator ignored", and the second sweep under
"The Kaizo study's worked examples"); Camouflage waits for Barry 3, in the
tracker's Scheduled list. Goal 2's fights and the three gyms were read
again on the fixed simulator, and only Fantina moved, harder by about 0.7
faints a fight through Drifblim's Unburden ("Goal 2 read again"). The Kaizo
study's five worked examples are read ("The Kaizo study's worked
examples"), and so is the Kaizo anchor, Kaizo's six readable bosses of its
first three splits on goal 2's boxes, which those boxes win 0 to 81 times
in 100 but for Fantina's second team ("The Kaizo anchor"). By Ian's
answers of 2026-10-04 a blind six now comes from the box's stronger half,
never a member held below the cap, and the Jubilife grunts' tag battle is
in Gardenia's split ("Ian's answers (2026-10-04)"). Goal 3 is held
until it follows the study's comb, by the tracker's Scheduled list. Every
reading is 75 fights at real odds and 25 very unlucky. The perfect-line store has been stale since the simulator
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

Left open, none changing a pick in the three gyms: the AI partners
beside the player and the switch rules in double battles were not ported;
Me First and Copycat need calculator rows of a Pokemon on itself; Judgment's
plate, Gravity, Foresight, Embargo and genders are not simulated, so the
routines reading them stay off (Magnet Rise, Torment and Pain Split were
simulated on 2026-10-03, when goal 2's fights met them: "Moves the
simulator ignored", below); in the strict search a
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

Ian checked it the same day: he is comfortable with the line for now, and
stage 2 of the speed plan starts (2026-10-02). The planner (`plplan.py`) played
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

Ian's answer on the wasted turns (2026-10-02, relayed by the Overseer): no
cost per turn goes into the position value for now. It would curb the wasted
turns but would also discourage stalling (a PP stall, waiting out a timed
effect), which wins fights; it stays an option for later. The value stays
faints, a loss, and survivors' HP. If stage 2's smoother value still leaves
the planner wasting turns, the evidence goes to Ian.

**Cost.** About 113 seconds of one core per fight and 24 decisions, so the 75
fights took 342 seconds on 29 workers (about 790 fights an hour). Each worker
holds at most about 190 MB.

## The network planner's Roark, for Ian's check (2026-10-02)

Goal 1, read again with stage 2's planner. It decides as the play-out planner
does, with the same exact look-ahead of one turn, but values each position
the turn can reach with the average of three networks (d1b+d2+d3, "Stage 2"
below) instead of playing the fight on from it. The networks learned their
values from the play-out planner's own play-outs. It played our hand-played
six and items (Barboach, Nidorino, Geodude with the Quick Claw, Onix,
Prinplup, Steenee, all at 16), and it meets our line's numbers.

**The numbers**, as in the play-out planner's write-up above (seeds from
2000; the planners' rows are 75 fights at real odds and 25 very unlucky, ours
2,000):

| Line | Dice | Clean | Won | Faints |
|---|---|---|---|---|
| Ours (the hand-played S12) | real odds | 98.5% | 100% | 0.015 |
| The network planner | real odds | 98.7% (74 of 75) | 100% | 0.013 |
| The play-out planner | real odds | 93.3% (70 of 75) | 100% | 0.067 |
| Ours | very unlucky | 96.4% | 99.95% | 0.043 |
| The network planner | very unlucky | 92% (23 of 25) | 100% | 0.080 |
| The play-out planner | very unlucky | 84% (21 of 25) | 100% | 0.160 |

Over 500 fights at real odds it reads 98.2% clean, every fight won, 0.020
faints, so its real-odds clean rate matches ours within a point. At the
bar's own size (for Ian's check, the same evening), 2,000 fights at real odds
read 97.7% clean, 100% won, 0.025 faints, and 500 very unlucky read 93.4%
clean, 100% won, 0.076 faints (`planner-net-d1b+d2+d3-roark-2000` and
`-unlucky-500`). By Ian's ruling of 2026-10-02, wins first and faints second,
it ties our line at real odds and beats it very unlucky (100% against
99.95%), with 0.010 and 0.033 more faints a fight. **Ian passed goal 1 on
this reading (2026-10-02): "close enough, pass".** Its one
faint at real odds was Onix to Cranidos; very unlucky, Onix to Cranidos and
Nidorino to Lileep. Twenty-five very unlucky fights cannot tell 92% from our
96.4% (two fights in 25 against one).

**How it chooses.** Before each turn it lists its options and works out the
trainer's choice exactly from the AI's own code, then weighs every chance in
the coming turn at its real odds, as before. Each position the turn can reach
is then valued by the networks in one batch, where the play-out planner
played the fight on from it about a hundred times. The value means the same:
minus one for each faint to come, minus ten more for a loss, plus a tenth of
each survivor's HP share. A fight costs about 3 seconds of one core, against
113.

**The line on the showcase seed (30)**, which it won cleanly
(`perfectline_results/step3/planner-net-roark-trace-seed30.txt` has every
turn and every option's value):

1. Geodude leads into Nosepass (-0.82, against -0.86 to -0.88 for the
   others), sets up Rock Polish while Nosepass Blocks, Defense Curls twice,
   and Magnitudes and Rock Throws it down.
2. Lileep comes in on Geodude, which is four times weak to Grass. It switches
   to Steenee (-0.70) rather than Prinplup (-0.75) or staying in (-0.82 at
   best). Steenee takes the Mega Drain resisted.
3. Steenee uses Play Nice (-0.57) rather than Razor Leaf (-0.71).
4. At 20 of 45 HP Steenee hands over to Nidorino (+0.25, against -0.52 at
   best for everything else). Nidorino Leers three times and Focus Energies
   once while Lileep Ingrains, then Double Kicks it out, ending on 18 of 47.
5. Roark's Geodude comes in on Nidorino. It brings Barboach in on the Thunder
   Punch it expects (+0.23, against -0.06 at best), and Mud Bombs Geodude to
   5 HP.
6. With Geodude on 5 HP, Barboach switches to Onix (+0.49) rather than
   finishing it with Water Gun (+0.25), so Onix makes the knockout and meets
   Cranidos. Onix spends seven turns on Geodude, now at +2 Defense (Rock
   Throw does 2 a hit), with Harden and Screech, then Screeches Cranidos to
   -6, Binds it three times and Rock Throws it out on 9 of 46 HP.

That is the play-out planner's line almost turn for turn, and close to ours
(we led Barboach into Nosepass).

**Checked against the play-outs.** The same fight was played again with the
network choosing and the play-out planner valuing every decision beside it
(`plplan roark --compare d1b+d2+d3 --drive network`;
`planner-net-roark-compare-driven-seed30.txt`). The two choose alike at 18 of
33 decisions, including every choice above (Steenee, Play Nice, Nidorino,
Barboach, Onix), and by the play-outs' own values the network's choices give
up 0.40 in all, 0.012 a decision. Where they differ, the options are within
about 0.05 of each other under the play-outs too, as close as play-outs can
measure.

**The nine ideas, as an exam.** Arose on its own, as with the play-out
planner: the free switch on a predictable pick (Steenee on Mega Drain,
Barboach on Thunder Punch), speed and status control (Play Nice, Leer,
Screech), the coverage hole (a Ground type against Thunder Punch), and the
hand-off at an HP that survives the next hit. Bait by knockout ownership
looks present but is not proven: in step 6 both planners pass up a sure
knockout so that Onix makes it and meets Cranidos, but the play-outs prefer
that by only 0.03 (+0.40 against +0.37), within their own noise, so I do not
count it. Did not apply at Roark: the PP stall, a timed effect, taking an
item, a sacrifice, and building the box.

**What it still does badly: the wasted turns.** Stage 2 did not cure them.
Rock Polish and two Defense Curls on turns 1 to 3, Focus Energy against
Lileep, seven turns on a 3-HP Geodude, and three Binds into a Cranidos at -6
Defense, where Rock Throw does more than twice the damage. These are not the
network's errors: under the play-outs those options read within 0.01 to 0.05
of attacking (the Binds exactly level with Rock Throw at +0.40). The value
has no cost for time, so a turn spent is free whenever the fight is safe.
Ian ruled (2026-10-02) that no cost per turn goes in for now, since it would
also discourage stalls that win fights, and that the evidence comes to him if
the smoother value still left the planner wasting turns; this is that
evidence. A cost per turn would cure it. A narrower option would only break
ties, preferring the option that ends the fight sooner among those the value
cannot tell apart, which leaves every stall that the value prefers.

Ian approved the narrower option (2026-10-02) on condition that it touch only
genuine ties and cost little. Built (`plplan --fast-tie`): among options tied
on the chance of losing and on faints, the one that takes most of the
trainer's HP this turn, a figure the look-ahead already has. Measured on
Roark over 2,000 fights at real odds with the network planner:

| Tie window | Clean | Won | Faints | Decisions | Core seconds a fight |
|---|---|---|---|---|---|
| off | 97.9% | 100% | 0.022 | 33.2 | 5.15 |
| the ranking's own tolerances | 89.5% | 99.95% | 0.115 | 21.7 | 2.47 |
| within 0.1 of the best value | 91.3% | 99.95% | 0.095 | 22.2 | 2.58 |
| within 0.02 of the best value | (wasted turns remain on the showcase seed) | | | | |

Any window wide enough to clear the showcase seed's wasted turns also costs
6 to 8 points of clean wins and four times the faints (in the 0.1 window,
Barboach falls to Cranidos 80 times, attacking where the default switches to
Onix), because the network's values differ by about 0.1 where the play-outs
call the options equal, so its ties are not genuine ones. It is therefore off
by default. It halves every reading's cost and turns, and since it shifts
every fight the same way it may keep their order; whether that trade is worth
it, against Ian's condition, is his call.

## The network planner's Gardenia, for Ian's check (2026-10-02)

A sanity check in the form of the Roark write-up above, read with the
network planner (d1b+d2+d3) under Ian's win-first ranking (`plplan` from
dfb60ab465 on, the faster-finish tie-break off), on our hand-played six and
items (Charmeleon, Popplio, Vikavolt, Kazza's Vullaby, Golbat with the Quick
Claw, Tsareena, all at 26).

**The numbers, ranked as Ian ranks them, wins first and faints second**
(network 500 fights at real odds and 200 very unlucky; play-out planner 75
and 25; ours 2,000):

| Line | Dice | Won | Faints | Clean |
|---|---|---|---|---|
| the play-out planner | real odds | 92% (69 of 75) | 2.787 | 1 of 75 |
| the network planner | real odds | 85.8% | 2.880 | 0.2% |
| ours (L1) | real odds | 59.9% | 3.212 | 15.1% |
| the play-out planner | very unlucky | 72% (18 of 25) | 3.560 | 0 |
| the network planner | very unlucky | 60% | 3.910 | 0.5% |
| ours | very unlucky | 30.1% | 4.680 | 4.8% |

By his order both planners beat our line on both dice, and the network
trails the play-out planner by about six points of wins. For ordering fights
it puts Gardenia where she belongs, far above Roark (100% won, 0.02 faints)
and Mars 1 (100%, 0.03).

**The line on the showcase seed (32)**, which it won with four faints
(`perfectline_results/step3/planner-net-gardenia-trace-seed32.txt`):

1. Vikavolt leads and Bug Bites Cherrim as the sun goes up; it switches to
   Charmeleon, which Scary Faces then Fire Fangs Cherrim out.
2. Lumineon comes in. Popplio takes the Aqua Tail and Sings it asleep (the
   play-outs' choice too: their chance of losing 0.24, the lowest), uses the
   sun's last turns on the sleeping Lumineon, and Icy Winds it as the sun
   ends; Lumineon gives way to Roserade.
3. Against Roserade the network sends Vullaby into Sludge Bomb, which leaves
   it at 2 HP and poisoned, where the play-outs send Golbat (their chance of
   losing 0.03 against 0.31). Popplio returns and faints; Charmeleon's Fire
   Fang takes Roserade.
4. Lumineon again: Charmeleon falls to Aqua Tail, and Vikavolt Sparks it out
   now that the sun is down (the play-outs agree, 0.11, their lowest).
5. Shiftry: Tsareena uses Magical Leaf twice, Teeter Dance and Play Nice
   where the play-outs would Stomp each turn, then the network switches a
   25-HP Vikavolt into Rock Tomb (their chance of losing 0.67 against 0.19
   for Stomp), losing it. Tsareena Stomps and falls; Golbat's Wing Attacks
   finish Shiftry and Breloom.

**The nine ideas, as an exam.** Arose: Charmeleon takes Cherrim, Popplio
Sings Lumineon, the sun's last turns spent on a sleeping foe, Vikavolt
Sparks Lumineon out after the sun, and Golbat closes out Shiftry and Breloom.
Not seen: Kazza's Pluck on Shiftry's Occa Berry, and Golbat walking in on
the Solar Beam charge.

**Checked against the play-outs** (`--compare d1b+d2+d3 --drive network`,
`planner-net-gardenia-compare-driven-seed32.txt`): the network chooses as
they would at 10 of 25 decisions, and by their estimates its other choices
add 1.735 to the chance of losing and 8.67 faints in all, the largest the
Vikavolt switch (+0.47), Spark into Lumineon with Vikavolt at full HP where
they would switch to Tsareena (+0.33), and Vullaby into Sludge Bomb (+0.28).
Those estimates come from the plain play-out policy, which loses Gardenia
far more often than either planner (its chances of losing run from 0.2 to
0.7 where the planners lose 8 to 14% of fights), so they show where the
network errs, not how much each error costs. Gardenia is where the network's
judgement is roughest, and the cheap labelling recipe did not mend it (two
spread rounds made it worse); the play-out planner is the better reader of
her for now.

## The play-out planner on Mars 1 and Gardenia (2026-10-02)

A baseline for goals 1 and 2 before stage 2 changes anything: the play-out
planner (budget 192 with racing) on our hand-played sixes, 75 fights at real
odds and 25 very unlucky, beside our lines over 2,000.

| Fight | Line | Dice | Clean | Won | Faints |
|---|---|---|---|---|---|
| Mars 1 | ours | real odds | 96.4% | 100% | 0.037 |
| Mars 1 | the planner | real odds | 97.3% (73/75) | 100% | 0.027 |
| Mars 1 | ours | very unlucky | 91.3% | 100% | 0.089 |
| Mars 1 | the planner | very unlucky | 92% (23/25) | 100% | 0.080 |
| Gardenia | ours | real odds | 15.1% | 59.9% | 3.212 |
| Gardenia | the planner | real odds | 1.3% (1/75) | 88% | 2.880 |
| Gardenia | ours | very unlucky | 4.8% | 30.1% | 4.680 |
| Gardenia | the planner | very unlucky | 0% (0/25) | 68% | 3.800 |

The planner meets Mars 1's bar. At Gardenia it is mixed: it almost never
wins cleanly, but it wins far more often than our line and loses fewer
Pokemon. Lumineon takes most of its losses (Charmeleon 32 times, Tsareena 16,
Vikavolt 14), and it leads Vullaby where we led Charmeleon. A fight costs
about 210 seconds of one core at Mars 1 and 160 at Gardenia.

## Goal 2: the rival fights of Roark's split (2026-10-02)

The first three of goal 2's new fights, read by the play-out planner (they
are short enough to need no network). Their boxes follow the Overseer's
provisional rule, until Ian confirms it: the captures from the areas reached
by each fight, every member at the split's cap of 16 as the run had it at
Roark, since the Pocket PC's Rare Candies make the cap reachable from Sandgem
on; Barry 1, before Sandgem, meets the starter alone at level 5. Lucas and
Dawn 1 (Route 202) is read without the Route 202 catch, which may come after
the fight; Barry 2 (the start of Route 203) after the Old Rod spots of
Twinleaf, Route 218 and Route 219 but before Route 203's own. No held items.

| Fight | Box | Real odds (75) | Very unlucky (25) |
|---|---|---|---|
| Barry 1 | Piplup at 5 (the run's, Gentle; Pound, Growl) against Turtwig | 0 clean, 0 won | 0 clean, 0 won |
| Barry 1 | Turtwig at 5 (Hardy; Tackle, Withdraw) against Chimchar | 75 clean | 25 clean |
| Barry 1 | Chimchar at 5 (Hardy; Scratch, Leer) against Piplup | 73 clean, 73 won | 25 clean |
| Lucas and Dawn 1 | Prinplup, Wooloo, Vulpix, Bibarel, Corvisquire at 16, each of the six variants | 75 clean each | 25 clean each |
| Barry 2 | five random sixes from the ten caught by then, at 16 | 75 clean each | 25 clean each |

Barry 1 is the game's first battle, and the engine gives it no critical hits
on either side: the Route 201 script starts it with StartFirstBattle, which
sets BATTLE_STATUS_FIRST_BATTLE, and BtlCmd_CalcCrit then sets the critical
multiplier to 1 (the Overseer, from the decomp, 2026-10-02). The simulator
now knows this (`fightsim.FIRST_BATTLE`, checked in `test_plfixes`), and the
readings above have it. The flag's other uses only change the touch screen's
background and route the move choice through the trainer AI, as in any
trainer battle. Losing it costs nothing in the game either: the script's lost
branch returns to the field with a different message, with no blackout. Ian
ruled (2026-10-02) that this first battle is the only fight in the game that
does not count for deaths or a wipe, so it is dropped from goal 2's fights
and its reading below is information only.

With a Piplup it cannot be won. Turtwig Withdraws, so Pound does 1 to 3 a
hit, and its Tackle, at the later games' 40 power and full accuracy (Oxide's
move numbers; Generation 4 had 35 and 95%), takes 5 of Piplup's 21 HP; the
look-ahead values every option, Growl included, as a certain loss from the
first turn. A neutral Piplup (Hardy) wins 1 of 75, so the run's Gentle
nature is not the cause. The cause is the base ROM's trainer data: Ian's
edit gives the Turtwig a Piplup player meets an IV scale of 144, IVs of 17,
where vanilla has 0. In-memory what-ifs (no data written) read Piplup's wins
out of 75 as 0 with Oxide's Tackle and Generation 4's alike, 1 with vanilla's
IVs alone, and 22 with vanilla's IVs and Tackle together: at level 5 the two
Tackles round to the same 5 damage. The other two starters win almost always. Lucas and
Dawn 1 and Barry 2 are over in a turn or two, as the cap makes them; that is
a true reading of Oxide as it stands, and flags them for the trainer pass.
Readings: `planner-barry_1-*`, `planner-lucas_dawn_1-v*` and
`planner-barry_2-six*` in the results folder (`plplan --six` and `--variant`
choose a six from the box and a rival's variant).

**Goal 2's fights and their caps (Ian, 2026-10-02).** Barry 1 and Lucas and
Dawn 1 are dropped (the first does not count, the second is trivial). The
interim soft caps sit at each mini-boss's ace until it is beaten: Barry 2 at
11, then Roark's split at 16, Mars 1 at 19, Gardenia's split at 26, Jupiter
1 at 27, Lucas and Dawn 2 at 30, Fantina's split at 33. Lucas and Dawn 2
cannot be fought before the Bicycle, so the order holds: its trigger
(Route 207, x 340, z 712 to 714, beside the Mt. Coronet entrance, live from
a new game until the scene sets `VAR_ROUTE_207_COUNTERPART_TRIGGER_STATE`)
lies above the route's bicycle slope (x 306, z 718 and 719). A flood fill of
Route 207's two map blocks (MAP_025 and MAP_026) from Oreburgh's edge,
counting only collision and the slope as walls, reaches the lower west
pocket alone; the trigger, the Mt. Coronet warp and Route 206's edge are out
of reach on foot, and the Bicycle comes after Jupiter 1. The Lucas and Dawn
files of Jubilife (ace 13) and Veilstone (ace 36) are battled by no map.

For the balance track (`splits.py` is theirs): it places Route 207's trainers
in Roark's split by the route's lower part, but all six (Camper Anthony,
Picnicker Lauren, Youngster Austin, Hikers Justin and Kevin, Battle Girl
Helen) stand above the bicycle slope too, as does Lucas and Dawn 2, so their
split should be the one after the Bicycle, Fantina's.

## Stage 2: the learned position value (from 2026-10-02)

Stage 2 of the speed plan replaces the planner's play-outs with a network
that values a position. The planner keeps its exact look-ahead of one turn
(the trainer's choice computed from its AI, every chance in the turn at its
real odds) and asks the network for the value of each position the turn can
reach, in one batch. The pieces are:

- `plfeat.py`: a position as 1,201 numbers and 144 ids (the field, the twelve
  Pokemon, and a matchup grid from the fight's calculator rows);
- `pldata.py`: labelled positions, from plain play-outs (the value the
  play-out planner averages), from the play-out planner's own look-ahead
  (`--distill`, or `--distill MODEL` with the network planner choosing), or
  from self-play (`--selfplay MODEL`: the network-guided planner's own
  fights, labelled by how they ended), and evaluation sets valued by many
  play-outs each (`--eval K`);
- `plnet.py`: training on the GPU in `~/venvs/oxide-ml`, with a check that the
  numpy export matches;
- `plvalue.py`: the network run with numpy in the planner's workers, and a
  check of its error against an evaluation set;
- `plplan.py --value MODEL` plays with the network, and `--compare MODEL`
  sets its values beside the play-outs' at each decision of a fight, with the
  regret of its choices.

**The data and weights live only outside git**, in
`~/oxide-trials/scorer-stage2/` (`data*/` shards, `models/`), and are rebuilt
from the code rather than kept. Each step is seeded, so it repeats:

```
PYTHONPATH=. tools/oxide/capped python3 -m tools.oxide.balance.pldata --sixes 30 --positions 20000
PYTHONPATH=. tools/oxide/capped python3 -m tools.oxide.balance.pldata --fights roark --hand --repeat 30 --positions 20000 --out ~/oxide-trials/scorer-stage2/data-roark-hand
PYTHONPATH=. tools/oxide/capped ~/venvs/oxide-ml/bin/python -m tools.oxide.balance.plnet --name v2 --data ~/oxide-trials/scorer-stage2/data ~/oxide-trials/scorer-stage2/data-roark-hand --held-out 3 --epochs 10
```

Training on the GPU is not bit-for-bit repeatable, so a retrained network
differs slightly from the one measured; its readings are measured again.

**First results (2026-10-02).** The first networks learned plain play-outs:
on our Roark six the best (v2) is off the true value by 1.45, about what three
play-outs give, against 0.2 for the planner's 192. Choosing with it, the
planner reads Roark at 45 of 75 clean, every fight won, 0.413 faints, against
the play-out planner's 70 of 75 and 0.067: it inherits the plain policy's
misreading of Lileep. It is fast: 2.7 seconds of one core a fight against
113, once numpy is held to one thread per worker.

**Self-play made it worse (2026-10-02).** Self-play, the speed plan's step
4, retrains the network on the network planner's own fights, each position
labelled by how its fight ended. Two rounds each played Roark worse than v2:
the first, exploring with any option, read 40 of 75 clean and lost 10 fights;
the second, exploring only among options near the best and continuing from
v2, read 3 of 75 clean and lost 25. A label that is one fight's outcome errs
by about 2.8, and the network learned that noise. Self-play is set aside.

**Distillation worked (2026-10-02).** The play-out planner already values
every position its look-ahead reaches, with up to a hundred play-outs each,
and those values are exactly what the network stands in for. `pldata
--distill` plays fights with the play-out planner and keeps every such
position, labelled by the mean of its play-outs; plnet weights each label by
how many there were, up to about five times a single play-out. The first set
(d1) is 1.2 million positions from 609 fights over ten sixes of each fight,
ours among them, and took 70 minutes on 29 workers. Trained from v2 on d1
together with the earlier plain play-out data, the network d1b plays as
follows on our sixes (clean, won, faints a fight; 75 fights at real odds, 25
very unlucky):

| Fight | Dice | Play-out planner | v2 | d1b |
|---|---|---|---|---|
| Roark | real odds | 70/75, 75/75, 0.067 | 45/75, 75/75, 0.413 | 69/75, 75/75, 0.093 |
| Roark | very unlucky | 21/25, 25/25, 0.160 | | 20/25, 25/25, 0.240 |
| Mars 1 | real odds | 73/75, 75/75, 0.027 | 49/75, 72/75, 0.733 | 64/75, 75/75, 0.293 |
| Mars 1 | very unlucky | 23/25, 25/25, 0.080 | | 16/25, 25/25, 0.520 |
| Gardenia | real odds | 1/75, 66/75, 2.880 | 0/75, 40/75, 5.013 | 1/75, 63/75, 3.227 |
| Gardenia | very unlucky | 0/25, 17/25, 3.800 | | 0/25, 16/25, 4.080 |

A fight costs d1b 2.4 seconds of one core at Roark, 3.4 at Mars 1 and 2.3 at
Gardenia, against 113, 210 and 160 for the play-out planner. At that speed
the whole game's 459 fights, 100 simulated fights each, take about an hour and
a half on 29 workers, before the spread of boxes for each boss. Its spot
check on one Roark fight (`plplan roark --compare d1b`): it chooses as the
play-outs do at 14 of 29 decisions (v2: 10), and its choices give up 0.039 a
decision by the play-outs' values (v2: 0.061), 0.22 at most. Trained on d1
alone (d1a) it reads Roark at 36 of 75, so the broad plain data still helps.

Mars 1 was the gap. There d1b plays lines the play-out planner never chose,
so d1 never labelled the positions it reaches. Round d2 let d1b play the
fights while play-outs labelled every position it looked at (`--distill
d1b`, the remedy known as DAgger), 1.2 million more positions, and d2 trained
from d1b on all of it. Seventy-five fights could not tell d1b and d2 apart, so
they were compared on 500 fights of each six at real odds, and so was their
average (`--value d1b+d2`, the mean of the two networks' values):

| Network | Roark | Mars 1 | Gardenia |
|---|---|---|---|
| d1b | 462 clean, 500 won, 0.088 | 398 clean, 496 won, 0.350 | 6 clean, 408 won, 3.490 |
| d2 | 417 clean, 500 won, 0.178 | 475 clean, 498 won, 0.088 | 8 clean, 407 won, 3.404 |
| d1b+d2 | 478 clean, 500 won, 0.050 | 483 clean, 497 won, 0.074 | 11 clean, 413 won, 3.436 |

d2 mended Mars 1 and lost ground at Roark; the average is better than either
everywhere, and at Roark better than the play-out planner (95.6% clean
against 93.3% on 75 fights). It costs 2.7 seconds of one core a fight at
Roark, 4.3 at Mars 1 and 2.7 at Gardenia.

Mars 1 still loses 3 fights in 500, where our line lost none in 2,000. The
play-out planner wins all three of those seeds cleanly, so the losses are the
network's misjudgements, not the dice. On seed 7307 the turn that starts it
is the third: Meowth has 19 HP left and Vullaby's Pluck did 28 the turn
before, yet the network values switching to Geodude (+0.24) above Pluck
(+0.17). Meowth then lives five more turns of Bite, Bronzor gets time to
stack Calm Mind behind Hypnosis, and Purugly sweeps a worn, sleeping team.
The play-out planner Plucks, and wins with no faint.

Round d3 did the same with the average d1b+d2 driving: 1.2 million more
positions from 790 fights (86 minutes), and d3 trained from d2 on all 5.9
million. Alone, d3 reads Mars 1 well (479 clean of 500) and Gardenia badly
(279 won, leading Vullaby). Averaged with the other two it is the best
planner so far, over 500 fights of each six at real odds:

| Network | Roark | Mars 1 | Gardenia |
|---|---|---|---|
| d3 | 456 clean, 500 won, 0.094 | 479 clean, 499 won, 0.084 | 0 clean, 279 won, 4.444 |
| d2+d3 | 432 clean, 499 won, 0.152 | 488 clean, 497 won, 0.060 | 0 clean, 293 won, 4.446 |
| d1b+d2+d3 | 491 clean, 500 won, 0.020 | 490 clean, 498 won, 0.044 | 11 clean, 423 won, 3.254 |

Its readings as Ian ruled them (75 fights at real odds and 25 very unlucky,
`planner-net-d1b+d2+d3-*` in the results folder), beside our hand-played
lines over 2,000 fights and the play-out planner:

| Fight | Dice | d1b+d2+d3 | Our line | Play-out planner |
|---|---|---|---|---|
| Roark | real odds | 74/75, 75/75, 0.013 | 98.5%, 100%, 0.015 | 70/75, 75/75, 0.067 |
| Roark | very unlucky | 23/25, 25/25, 0.080 | 96.4%, 99.95%, 0.043 | 21/25, 25/25, 0.160 |
| Mars 1 | real odds | 74/75, 75/75, 0.013 | 96.4%, 100%, 0.037 | 73/75, 75/75, 0.027 |
| Mars 1 | very unlucky | 24/25, 25/25, 0.080 | 91.3%, 100%, 0.089 | 23/25, 25/25, 0.080 |
| Gardenia | real odds | 0/75, 62/75, 3.360 | 15.1%, 59.9%, 3.212 | 1/75, 66/75, 2.880 |
| Gardenia | very unlucky | 0/25, 14/25, 4.480 | 4.8%, 30.1%, 4.680 | 0/25, 17/25, 3.800 |

It meets the Roark and Mars 1 bars, with the very unlucky Roark at 23 of 25
where ours is 96.4% (25 fights cannot tell those apart). At Gardenia it
behaves as the play-out planner does: it wins more often than our line and
almost never cleanly, which is the open question in the tracker of how a
loss should weigh against a faint. A fight costs it 2.6 to 3.8 seconds of
one core, three network passes a decision.

**A network cannot yet judge a trainer it has not seen.** Two networks were
trained from scratch by one recipe on every shard so far, one with
Gardenia's and one with Roark's and Mars 1's only (`plnet --fights`), and
both were read on 500 fights of each six at real odds:

| Network | Gardenia | Mars 1 |
|---|---|---|
| with Gardenia's data | 0 clean, 362 won, 3.854 | 475 clean, 500 won, 0.060 |
| without it | 0 clean, 2 won, 5.994 | 487 clean, 500 won, 0.028 |

Without Gardenia's positions it loses almost every Gardenia fight. Trained
on three trainers, it has never met most of the game's species and moves,
so its ids for them mean nothing. Every new fight therefore needs labelled
positions of its own before the network can play it: for goal 2, a round of
distillation for the rival fights, Jupiter 1 and Fantina.

**Trained on many trainers, it does judge unseen ones (2026-10-02).** The
test (`plgen.py`) took the 100 ordinary singles trainers of Roark's,
Gardenia's and Fantina's splits (gym leaders' rematch teams left out), held
out every fifth, and labelled the other 80 with the play-out planner on four
random boxes each (`fightsim.random_box`, the blind reading's boxes), 1.65
million positions in ten minutes on 29 workers. Networks trained from
scratch on those and the gyms' three distillation rounds were read on the 20
held-out trainers, on a box none of the data used, 40 fights each at real
odds:

| Planner | Clean | Won | Faints a fight |
|---|---|---|---|
| the play-out planner | 800 of 800 | 800 | 0.000 |
| a network without the held-out trainers (seed 1) | 767 | 799 | 0.065 |
| the same with them (seed 1) | 768 | 793 | 0.110 |
| a network without them (seed 2) | 787 | 800 | 0.020 |
| the average of the two without them | 789 | 800 | 0.015 |

Having seen the held-out trainers made no difference: the networks' misses
fall on different trainers from one network to the next (Aroma Lady Hannah
19 clean of 40 under one, 35 under another), so they are each network's own
noise, and averaging two networks that never saw these trainers comes within
about a point of the play-out planner.

These were easy fights, though (the Overseer's caution): the ordinary
trainers of the first three splits read nearly all clean at the cap, under
play-outs 800 of 800. The harder test is a held-out boss. Two networks
trained from scratch on everything except Gardenia's positions (the 100
ordinary trainers, and Roark's and Mars 1's three distillation rounds;
`plnet --without gardenia`) were read at Gardenia on our six, 500 fights at
real odds:

| Network, without Gardenia's positions | Clean | Won | Faints a fight |
|---|---|---|---|
| seed 1 | 2 of 500 | 7 | 5.950 |
| seed 2 | 0 | 11 | 5.934 |
| the average of the two | 0 | 8 | 5.960 |

against 413 won for the networks that saw her (d1b+d2+d3 won 423) and 66 of
75 for the play-out planner. A boss brings what the early ordinary trainers
never show (sun with Chlorophyll, Natural Gift and its berries, a six built
to work together), and without positions from her fight the networks
misjudge it from the lead on (they lead Golbat). So for the whole game,
ordinary trainers can lean on broad data and one labelling pass, but every
boss needs labelled positions of its own, with rounds from the network's own
play as Mars 1 needed.

The Mars 1 lead values are all equal, under play-outs and networks alike,
and that is the fight, not a fault: from any lead the best first move is to
switch to Vullaby into Meowth's Fake Out, so every lead reaches the same
position. The commands that rebuild d1b:

```
PYTHONPATH=. tools/oxide/capped python3 -m tools.oxide.balance.pldata --distill --sixes 10 --repeat 3 --positions 12000 --seed 1 --out ~/oxide-trials/scorer-stage2/data-d1
PYTHONPATH=. tools/oxide/capped --max 20G ~/venvs/oxide-ml/bin/python -m tools.oxide.balance.plnet --name d1b --from v2 --data ~/oxide-trials/scorer-stage2/data-d1 ~/oxide-trials/scorer-stage2/data ~/oxide-trials/scorer-stage2/data-roark-hand --held-out 1 --epochs 6 --lr 5e-4
```

And d2 and d3 after it (each round's labels come from the planner the last
round made; `S` is `~/oxide-trials/scorer-stage2`):

```
PYTHONPATH=. tools/oxide/capped python3 -m tools.oxide.balance.pldata --distill d1b --sixes 10 --repeat 3 --positions 12000 --seed 2 --out $S/data-d2
PYTHONPATH=. tools/oxide/capped --max 22G ~/venvs/oxide-ml/bin/python -m tools.oxide.balance.plnet --name d2 --from d1b --data $S/data-d2 $S/data-d1 $S/data $S/data-roark-hand --held-out 1 --epochs 6 --lr 5e-4
PYTHONPATH=. tools/oxide/capped python3 -m tools.oxide.balance.pldata --distill d1b+d2 --sixes 10 --repeat 3 --positions 12000 --seed 3 --out $S/data-d3
PYTHONPATH=. tools/oxide/capped --max 22G ~/venvs/oxide-ml/bin/python -m tools.oxide.balance.plnet --name d3 --from d2 --data $S/data-d3 $S/data-d2 $S/data-d1 $S/data $S/data-roark-hand --held-out 1 --epochs 6 --lr 5e-4
```

## Wins first, then faints (Ian, 2026-10-02)

Ian ruled that a fight ranks by its win rate first and its average faints
second, the clean rate reported but not optimised: "a fight with 0% clean,
100% win, and 1.00 average faints means that a single sac wins the fight
every time, and I would take that every time over a 90% clean, 90% win
chance with 0.60 average deaths". The old value's loss weight of ten let a
point of win rate trade for a tenth of a faint, which his order forbids. The
same order judges a line against a bar.

The planner now ranks its options that way (`plplan.choose`). Each option's
chance of losing and faints expected come from its play-outs' ends, or with
a network from its loss and faints heads (which the labels already trained,
from the parts they keep). Options within 0.05 of the lowest chance of
losing count as tied on it, since on positions they never trained on the
networks' estimate of that chance errs by 0.051 at Gardenia and 0.080 at
Mars 1 (labels' own error about 0.016); among those, options within 0.1 of
the fewest faints count as tied on faints, and the old value, which carries
the survivors' HP, decides the rest. `--rank value` restores the old ranking.
The network planner (d1b+d2+d3), 500 fights at real odds each:

| Fight | Ranking | Clean | Won | Faints |
|---|---|---|---|---|
| Gardenia | the old value | 11 | 423 | 3.254 |
| Gardenia | Ian's order | 1 | 429 | 2.880 |
| Gardenia, very unlucky (200) | the old value | 0 | 125 | 4.205 |
| Gardenia, very unlucky (200) | Ian's order | 1 | 120 | 3.910 |
| Roark | the old value | 491 | 500 | 0.020 |
| Roark | Ian's order | 492 | 500 | 0.016 |
| Mars 1 | the old value | 490 | 498 | 0.044 |
| Mars 1 | Ian's order | 492 | 500 | 0.020 |

Ian's order wins as often or a little more (the Gardenia differences are
within the noise of 500 fights) and loses fewer Pokemon at all three. The
readings before this section used the old value.

## The team search: plan and costs (for Ian, 2026-10-02)

Ian ruled that the scorer's job is to order every fight correctly by
difficulty, close enough, and that for a boss it chooses its own six and
moves: a screen with no simulated fights, a race among the screen's top
twenty or so, and the full reading of two or three finalists; his idea for
the race rates each box member by how the sixes it is drawn into fare (the
cross-entropy method over members); and his loop, with the Overseer's
additions, sends what the finalist reading learns back to the race. This is
the plan, with every cost from a measurement of the same day.

**What the costs rest on.** One simulated fight costs the play-out planner
113 seconds of one core at Roark, 210 at Mars 1 and 212 at Gardenia (300 very
unlucky); the network planner, 2.5 to 4. A boss's labels cost about 1.7
core-hours by the cheap recipe where it holds (Mars 1) and about 28 for three
full rounds (Gardenia, where the cheap recipe failed: 334 won of 500 after
one spread round and 299 after two, against 429 for the full rounds and 69
of 75 for the play-out planner). And labels carry between sixes of one fight:
networks that saw Mars 1's labels from nine other sixes but never ours read
our six at 463 clean of 500, every fight won, 0.084 faints, against 490, 499
and 0.032 for networks that saw it. Wins hold; the clean rate drops five
points. That is close enough to rank sixes in a race, so the race can run on
the network.

**The stages.**

1. *Screen, no simulated fights.* The damage calculator's rows for every box
   member's whole learned move pool against every enemy, both ways, with
   speed: for each pair, the hits each side needs and who moves first. Each
   member's four moves are picked against this fight from its pool (three
   attacks of different types and the best status move, by the scorer's
   rule, weighted to the enemies it answers). Sixes are built to answer
   every enemy (a member that knocks it out in fewer hits than it needs, or
   that outspeeds it and survives), with the least overlap, by a greedy
   build and swaps, and the top twenty go on. About a core-minute per boss
   and box, mostly the calculator.
2. *Labels for the fight.* The screen's top sixes, from every box to be
   read, are labelled together: the cheap recipe spread over them (a tenth
   of a round across about ten sixes, then one spread round from the
   network's own play over the twenty), about 1.7 core-hours a boss.
3. *Race, on the network.* Ian's member ratings: sixes are drawn by member
   weights, each read on four fights, and the weights move toward the
   members of the best sixes, five rounds of sixteen sixes (320 fights,
   about 0.3 core-hours); then the best five full sixes race by halving
   (about 0.2) to settle pairs that work only together.
4. *Finalists.* Two or three sixes, 100 fights each (75 real, 25 very
   unlucky) on the network, about 0.3 core-hours.
5. *Diagnose and loop.* The winner is also read by the play-out planner on
   25 fights (about 1.4 core-hours). If the network falls short of it on the
   same six, the gap is training: one more spread round on that six (0.7),
   then read again. If both fall short together, the six is the problem: the
   enemies that cause its faints and losses raise the ratings of members
   that answer them, the full reading weighs more than a race fight, and the
   race runs again. Stop when a loop no longer improves the best six beyond
   noise, or after three loops.

**Totals.** Per boss and box, stages 1, 3 and 4 cost about 0.5 core-hours;
per boss, the labels about 1.7 and the diagnosis about 1.4. For goal 3's 38
kept bosses (its 79 rows less the 41 Ace Trainers) on five boxes each, that
is about 38 x (1.7 + 1.4 + 5 x 0.5), some 210 core-hours, about 7 hours on
29 workers, if the cheap recipe holds everywhere. Where it fails as at
Gardenia, the race itself ran on a weak network, so its ranking is suspect
as well as the finalist's reading (the Overseer's check): there the play-out
planner reads the race's top three on 25 fights each (about 4.2 core-hours)
and then the best of them in full (about 5.6), some 10 core-hours per boss
and box, rather than three full rounds of labels (28 a boss). If a quarter
of the bosses need it on each box, add about 38 x 0.25 x 5 x 10, some 470
core-hours, about 16 hours more; reading those bosses on fewer boxes cuts it
in proportion. The Ace Trainers take the whole cheap recipe each (1.7
core-hours: at Fantina's split, Allen still read 80 clean of 100 against the
play-out planner's 99 after about 106,000 of his own positions, so a tenth
of a round alone is not enough), about 70 core-hours, some two and a half
hours more.

**Which planner where.** The network wherever there is a race, since a race
on the play-out planner alone costs about 13 core-hours per boss and box
(some 240 fights at 200 seconds) and the whole of goal 3 that way would take
weeks. For a single fixed six read once, the network still pays (1.8
core-hours with its labels against 5.6 for play-outs) where the cheap recipe
holds; where it does not, the play-out planner reads the finalist.

**Two further options, costed, not started (Ian's brainstorm, relayed).**

*A general boss network.* One value network trained on many varied boss-like
fights, so that it reads a boss it has never seen and a boss needs no labels
of its own: the game's own bosses across many sixes, the Kaizo study's
trainer sheets, and boss-like teams built from the trainer palette, perhaps
300 fights in all. At a tenth of a round each at budget 64 (about 40,000
positions, 0.6 core-hours), the one-off labelling is about 180 core-hours,
some 6 hours on 29 workers; the pile, about 12 million positions, needs a
loader that streams it rather than holding it in memory (the present one
holds about 6 million). The test is held out: train without Gardenia and
Mars 1 at 19 and read both. If they read close enough, it saves every boss's
own labels (about 2 hours for goal 3's 38, plus the play-out fallback where
the cheap recipe fails, about 9 more) and the 4 minutes per fight at every
trainer-pass change after, and the race and the reading run at about 3
seconds a fight. The risk is the same test failing as it did today: trained
on 100 easy trainers and two bosses, the network won 8 Gardenia fights of
500. Hundreds of hard, varied fights may be what it lacked, and only the test
will say.

*A learned stand-in for the play-outs.* A small policy network that picks
each turn's move as the play-out planner would, trained on its own choices,
to replace the plain policy inside the play-outs. Play-outs that play more
like the planner value positions more truly, so fewer of them would do: if a
budget of 24 then chose as well as 64 or 192 does now, the play-out planner
gets about three times cheaper, which brings a finalist's 100-fight reading
from about 5.6 core-hours to about 2 and a boss's labels from about 1.7 to
about 0.6. Its labels are the planner's decisions, which the shards do not
yet keep: recording them over about 2,000 play-out fights of the bosses is
about 80 core-hours (3 hours), and training is minutes. A stand-in costs
about as much per turn as the plain policy (one small forward pass), and
whether it makes a smaller budget choose as well is a measurement, the
choices agreeing at the showcase seeds as the spot check counts them.

**The first test (the Overseer's).** The search on the hand run's own boxes
at Roark, Mars 1 (at 19) and Gardenia, to see whether it finds our sixes or
ones that read as well by wins and then faints. Roark and Gardenia have
labels across ten sixes already; Mars 1 at 19 needs its own. A miss at Mars
1, which our six wins by a PP stall, would show the screen undervaluing stall
plans. **Building it** is the screen (the largest piece), the race with
member ratings, and the loop; the first test runs on what is there.

## The team search's first test (2026-10-02)

The search is built (`plteam.py`, with its test runner `plteam_test.py`) and
ran once on each of the hand run's boxes. At Gardenia it found a six that
reads better than ours, and at Mars 1 one that reads about as well, but at
Roark it chose a six that reads worse than ours, because its networks misread
every six unlike the ones they were trained on. Two fixes follow, and Roark
runs again.

Each fight's box is the run's box at that fight, every member with its whole
move pool by the capture rule. The screen picks each member's four moves
against the fight, so the search's sixes and ours carry the screen's moves,
not the hand line's. The labels were a tenth of a round at budget 64 over the
screen's top ten sixes; the networks were trained from scratch on every
earlier label except that fight's, plus the new ones. The play-out planner
then read the race's winner on 25 fights.

| Fight | The search's winner | Network, 75 real | Play-outs, 25 | Our six by play-outs | Minutes |
|---|---|---|---|---|---|
| Roark | Prinplup, Krabby, Nidorino, Onix, Charmander, Geodude | 100% won, 0.00 faints | 100% won, 0.60 faints, 40% clean | 100% won, 0.07 faints, 93% clean | 20 |
| Mars 1 at 19 | Prinplup, Vullaby, Finneon, Nidorino, Onix, Geodude | 100% won, 0.20 faints | 96% won, 0.28 faints, 92% clean | the bar: 99.8% won, 0.42 faints | 44 |
| Gardenia | Dubwool, Bibarel, Corvisquire, Wartortle, Tsareena, Golbat | 89% won, 2.01 faints | 100% won, 1.52 faints, 16% clean | 92% won, 2.79 faints | 18 |

Our six by play-outs is the play-out planner's reading of 75 fights with the
hand line's moves and items; at Mars 1 at 19 the bar is our line adjusted.
The minutes are wall time on ten workers. That column is not like for like:
the search gives every six the screen's moves and the simulator's item rule
(a type booster, Leftovers or a Sitrus Berry while copies last), so at Roark
our six plays with Pound, Peck, Tackle and Tackle in place of the hand line's
Growl, Leer, Bind and Defense Curl, and without Geodude's Quick Claw. The
fixed runner reads our six that way too.

**Roark.** The networks read our six (with the screen's moves) at 52% won and
3.5 faints, and every one of the three finalists at 100% won. The play-outs
read the winner at 0.60 faints against our six's 0.07. The cause is the
labels: the screen's top ten sixes all share Onix and Geodude, and eight of
them each carry Nidorino and Charmander, so the networks learned that core's
fights well and had few labels from sixes without it. Our six (Prinplup, Barboach, Nidorino,
Onix, Steenee, Geodude) ranked 162nd of 8,008 in the screen.

**Mars 1 at 19.** The screen ranked our six 1,831st of 38,760, which confirms
that it undervalues the PP stall our line wins by: it counts hits, and a stall
wins on turns. The race recovered: Vullaby, the stall's centre, ended with the
highest member weight, and the winner keeps Vullaby, Nidorino, Onix and
Geodude from our six. Its faints fell mostly to Purugly (10 of 25 fights).

**Gardenia.** The network read the winner at 89% won, the play-outs at 100%,
so here it was too harsh. The winner beats our six by play-outs on both
numbers (100% won against 92%, 1.52 faints against 2.79); its faints fell to
Roserade and Cherrim. Our six ranked 1,644th of 100,947 in the screen.

**The fixes.** The network erred both ways, too kind at Roark and too harsh at
Gardenia, so its race is a shortlist and not a verdict.

1. The labels now come from the screen's top five sixes and five sixes drawn
   at random from the box, so the networks have seen fights unlike the
   screen's favourite core.
2. The play-out planner reads every finalist and our six on 25 fights as a
   standard step, not only when the recipe fails, and the winner is the
   finalist it ranks best by wins and then faints.

The second adds about three finalist readings of 25 fights each, some 4
core-hours per boss and box, which goal 3's totals must carry. The rerun at
Roark tests both.

**The rerun at Roark, with both fixes.** The search found a six that reads as
well as ours. The play-out planner on 25 fights each:

| Six | Won | Faints | Clean | The network, 75 real |
|---|---|---|---|---|
| Wooloo, Barboach, Nidorino, Onix, Charmander, Geodude (the winner) | 100% | 0.12 | 88% | 100%, 0.17 |
| Bibarel, Finneon, Nidorino, Onix, Charmander, Geodude | 100% | 0.48 | 52% | 100%, 0.39 |
| Corvisquire, Dottler, Nidorino, Onix, Charmander, Geodude | 100% | 0.32 | 68% | 100%, 0.45 |
| our six, with the screen's moves | 100% | 0.12 | 88% | 83%, 1.76 |

The winner's three faints in 25 fights all fell to Roark's Geodude. The
networks now read the finalists close to the play-outs, but they still read
our six far too harshly (83% won against 100%). Our six was not among the ten
labelled sixes, so a race on the network can still pass over a good six it
has no labels for; the play-out check corrects the finalists, not the race.
Here the race found an equal six anyway. The run took 33 minutes on ten
workers, 17 of them in the play-out check (100 fights, about 100 core
seconds each).

**The rerun at Mars 1 at 19.** The search found sixes better than ours. All
three finalists keep Vullaby, the stall's centre, with Onix and Geodude, and
the play-out planner won every one of their 25 fights each with nothing
fainting:

| Six | Won | Faints | Clean | The network, 75 real |
|---|---|---|---|---|
| Prinplup, Bibarel, Vullaby, Onix, Charmander, Geodude (the winner) | 100% | 0.00 | 100% | 100%, 0.23 |
| Wooloo, Vullaby, Barboach, Krabby, Onix, Geodude | 100% | 0.00 | 100% | 97%, 0.40 |
| Prinplup, Vullaby, Wartortle, Krabby, Onix, Geodude | 100% | 0.00 | 100% | 96%, 0.48 |
| our six, with the screen's moves | 100% | 0.32 | 80% | 99%, 0.23 |

Here the network was too harsh on the finalists rather than too kind, and it
placed our six level with the best of them; only the play-outs separated
them. The play-out check took 74 minutes on ten workers, about 440 core
seconds a fight, twice the earlier measure (the stall makes long fights, and
the machine was near full load beside the stand-in's recording).

**The rerun at Gardenia.** The search found a six a little better than ours,
keeping Vullaby, Charmeleon, Tsareena and Golbat from our six:

| Six | Won | Faints | Clean | The network, 75 real |
|---|---|---|---|---|
| Dubwool, Bibarel, Vullaby, Charmeleon, Tsareena, Golbat (the winner) | 96% | 1.52 | 16% | 89%, 2.15 |
| Prinplup, Dubwool, Bibarel, Vullaby, Tsareena, Golbat | 96% | 2.28 | 0% | 92%, 1.72 |
| Dubwool, Bibarel, Barboach, Wartortle, Tsareena, Golbat | 96% | 1.84 | 0% | 88%, 2.24 |
| our six, with the screen's moves | 96% | 1.88 | 12% | 87%, 2.40 |

The winner's faints fell mostly to Roserade (27 of 38). On 25 fights the gap
to our six is within noise; both are well above our hand line's bar (59.9%
won, 3.21 faints), which is the bar of a person playing, not of the planner.

**The answer to the first test.** With both fixes, the search found our six's
equal at Roark and sixes better than ours at Mars 1 at 19 and at Gardenia,
each judged by the play-out planner with every six on the same moves and
items. Two cautions stand: the network still misreads sixes far from the
labelled ones (our six at Roark), so the race can pass over a good six; and
items are not searched.

**What a boss costs now.** Measured on the reruns, per boss and box, on ten
workers beside the recording:

| Stage | Roark | Mars 1 at 19 | Gardenia |
|---|---|---|---|
| labels, ten sixes (core-hours) | 1.2 | 1.6 | 0.9 |
| two networks (GPU minutes) | 5 | 5 | 5 |
| race and finalists on the network (core-hours, about) | 0.8 | 0.8 | 0.8 |
| play-out check of three finalists (core-hours) | 2.2 | 9.2 | 2.1 |
| wall time of the whole run (minutes) | 33 | 94 | 30 |

That is about 6.5 core-hours per boss and box, against the plan's 2.5, most
of it the play-out check. For goal 3's 38 bosses on five boxes each it comes
to about 1,230 core-hours, some 42 hours on 29 workers, plus about 17 hours
of GPU for 190 pairs of networks (which can run beside the CPU work), and
about 70 core-hours for the Ace Trainers. The levers, none yet measured:

1. One label set and one pair of networks per boss, its ten sixes spread over
   the five boxes, in place of ten sixes per box: about 1,050 core-hours, and
   3 GPU hours.
2. The play-out check on the top two finalists, not three: about 770.
3. A smaller play-out budget. The learned stand-in player failed its test,
   and budget 24 with the plain policy holds only in easy fights, but
   budget 64 chose about as well as 192 at all three gyms ("The learned
   stand-in player, and smaller budgets", below). The check at 64 brings the
   total to about 630 core-hours (before the Ace Trainers); this one waits
   on Ian.

**Held items are not searched.** The simulator's item rule knows only type
boosters, Leftovers and Sitrus Berries, so a six never holds the run's
Quick Claw, and goal 3's bosses will come after element 7's held items
(Eviolite, Assault Vest and the rest) are placed behind optional fights. A
proposed later step: the finalists try the box's held items, each read
by the network, before the play-out check.

## The learned stand-in player, and smaller budgets (2026-10-03)

The stand-in failed its test, and the plain policy at a smaller budget
nearly passed it. The stand-in was meant to make the play-out planner
cheaper: play-outs played more like the planner would value positions more
truly, so a budget of 24 might choose as well as 192. A small budget with
the plain policy is the obvious thing to compare it with, and that
comparison decided it.

**The stand-in.** Its data is the play-out planner's own decisions at the
three gyms (`pldata --choices`). The recording was slower than estimated
beside the team search, and stopped after 27 of its 90 jobs, about 16,500
decisions; the early networks were trained on those. Their agreement with
the planner's choices on held-out decisions, where a random legal pick
agrees 17% of the time and two full-budget planners about 74 to 86%:

| Stand-in | Agreement | Its pick, per turn |
|---|---|---|
| compact (the field, the two active Pokemon, the matchup grid) | 50% | about 230 microseconds |
| full (the value network's body, started from d1b) | 64% | about 11,000 microseconds |

A whole simulated turn with the plain policy costs about 150 to 225
microseconds, so the full stand-in cannot play play-outs at any useful
speed, and the compact one makes a turn two to three times dearer.

**The budget check** (`plplan --budget-check`): fights played by the full
planner (budget 192); at each decision, a second full-budget planner on dice
of its own, budget 24 with the plain policy, and budget 24 with the compact
stand-in choose too, and their choices are scored by the full planner's own
estimates. At Roark, 12 fights, 265 decisions:

| Planner | Same choice | Chance of losing added | Faints added | Seconds a decision |
|---|---|---|---|---|
| budget 192 again (the ceiling) | 74.0% | +0.005 | +2.4 | 4.1 |
| budget 24, plain | 70.6% | +0.046 | +3.6 | 1.2 |
| budget 24, the compact stand-in | 55.1% | +0.008 | +23.2 | 2.9 |

The added chances and faints are totals over all 265 decisions. Two full
planners disagree on a quarter of decisions at almost no cost, since many
options are near equal. Budget 24 with the plain policy chooses almost as
well, at a quarter of the cost. The stand-in's play-outs judge positions
worse than the plain policy's, adding 23 faints, and cost two and a half
times as much as the plain ones at the same budget, so even a perfect
stand-in at 24 would cost about what the plain policy does at 60. More of
its data might lift its agreement a few points, but not across a gap this
size, so the recording is stopped (its shards are kept in `data-choices`).

**Budgets 24 and 64 at Mars 1 and Gardenia,** with the plain policy, 12
fights each, the same check:

| Fight | Planner | Same choice | Chance of losing added | Faints added | Seconds a decision |
|---|---|---|---|---|---|
| Mars 1 (341 decisions) | budget 192 again | 59.5% | +0.009 | +9.4 | 3.4 |
| | budget 64 | 56.6% | +0.017 | +8.5 | 1.0 |
| | budget 24 | 48.4% | +0.023 | +11.7 | 0.6 |
| Gardenia (280 decisions) | budget 192 again | 71.4% | +4.5 | +9.8 | 3.0 |
| | budget 64 | 64.6% | +4.8 | +14.2 | 0.9 |
| | budget 24 | 58.9% | +9.4 | +27.6 | 0.5 |

At Mars 1 the PP stall leaves many options near equal, so even two full
planners agree on only 60% of decisions; budget 64 matches the second full
planner and 24 is a little worse. At Gardenia the full planner's own
estimates of losing are noisy (the plain policy loses her often from many
positions), so a second full planner "adds" 4.5 in all; budget 64 sits at
that ceiling for losing and a little above it for faints, and budget 24
doubles both. So budget 24 is good enough only where the fight is easy,
and budget 64 chooses about as well as 192 at all three gyms, at a quarter
to a third of the cost.

**The check itself at budget 64.** The three gyms' finalists and our six,
read again at budget 64 on the same 25 seeds as the reruns' budget-192
check:

| Fight | Six | Budget 64 | Budget 192 |
|---|---|---|---|
| Roark | Wooloo, Barboach, Nidorino, Onix, Charmander, Geodude | 100% won, 0.20 faints | 100%, 0.12 |
| | Bibarel, Finneon, Nidorino, Onix, Charmander, Geodude | 100%, 0.48 | 100%, 0.48 |
| | Corvisquire, Dottler, Nidorino, Onix, Charmander, Geodude | 100%, 0.44 | 100%, 0.32 |
| | our six | 100%, 0.28 | 100%, 0.12 |
| Mars 1 at 19 | Prinplup, Bibarel, Vullaby, Onix, Charmander, Geodude | 100%, 0.00 | 100%, 0.00 |
| | Wooloo, Vullaby, Barboach, Krabby, Onix, Geodude | 100%, 0.08 | 100%, 0.00 |
| | Prinplup, Vullaby, Wartortle, Krabby, Onix, Geodude | 100%, 0.08 | 100%, 0.00 |
| | our six | 100%, 0.24 | 100%, 0.32 |
| Gardenia | Dubwool, Bibarel, Vullaby, Charmeleon, Tsareena, Golbat | 96%, 1.80 | 96%, 1.52 |
| | Prinplup, Dubwool, Bibarel, Vullaby, Tsareena, Golbat | 84%, 2.20 | 96%, 2.28 |
| | Dubwool, Bibarel, Barboach, Wartortle, Tsareena, Golbat | 100%, 1.96 | 96%, 1.84 |
| | our six | 92%, 1.84 | 96%, 1.88 |

The two budgets pick the same winner at Roark and Mars 1. At Gardenia they
do not, but the cause is the reading's size, not the budget: on 25 fights
one loss moves the win rate four points, and the same six reads 84% at one
budget and 96% at the other. The check ranks wins first with no tolerance,
so one fight's luck (100% against 96%) chose the winner at 64. The planner's
own choice among options already treats chances of losing within 0.05 as
equal before it compares faints (`plplan.LOSS_TOL`); with the same
tolerance for the finalists, both budgets pick the same winner at all three
gyms (at 64, the Barboach six's 100% and the Vullaby six's 96% count as
equal, and the Vullaby six wins on 1.80 faints against 1.96).

**For Ian: budget 64 for the play-out check, and a tolerance on wins.** The
team search's play-out check, and any play-out reading, would run at budget
64 in place of 192 (the labels are already at 64), and its finalists would
be ranked as the planner ranks options: win rates within 0.05 count as
equal, then the fewest faints. That brings the check from about 4.5
core-hours per boss and box to about 1.3, and goal 3 from about 1,230
core-hours to about 630 before the Ace Trainers, some 22 hours on 29
workers, or about 450 with one label set per boss (lever 1). It changes how
the scorer reads a fight, so it waits on Ian's word; goal 2's readings ran
at 192. The loop added later (below) adds up to six 25-fight readings
where the winner loses Pokemon, about 6 core-hours at Fantina.

## Moves the simulator ignored (2026-10-03)

Lucas and Dawn 2's first winning line showed Whiscash's Magnitude knocking
out a Jolteon that had used Magnet Rise four turns running: the simulator
had no Magnet Rise, so the move did nothing and the AI, seeing no rise,
chose it again. A sweep of every trainer move in the 33 story fights for
effects the simulator never names found the rest. These are now simulated
as the engine has them, each with a check in `test_plfixes` (52 of 52
pass):

- Magnet Rise (Lucas and Dawn 2's Jolteon): five turn ends in which Ground
  moves fail on the user, cleared by a switch, failing while active, on a
  Levitate user or under Ingrain (effect script 252, and the type check's
  `MOVE_STATUS_MAGNET_RISE`).
- Torment (Lucas and Dawn 2's Monferno): the target cannot pick the move it
  used last until it switches, in the player's options, the play-out
  policy and the trainer's AI alike (`CHECK_INVALID_TORMENTED`).
- Pain Split (Fantina's Rotom): both Pokemon's HP become half their sum,
  failing on a Substitute (`subscript_pain_split`).

- Destiny Bond (2 fights not yet read; one of the forced trades Ian's
  design rules allow a boss): a foe whose move faints the bonded Pokemon
  faints too, unless the move's recoil already felled it; the bond ends
  when its user next tries to act or switches out (`subscript_destiny_bond`,
  `subscript_faint_check_destiny_bond`).

These make the trainers stronger, so Lucas and Dawn 2 and Fantina are read
again on the fixed simulator; the earlier Lucas and Dawn 2 reading is kept
as `team/lucas_dawn_2-oldsim`. (Destiny Bond went in after the reruns
started; neither fight has it.)

**Genders, Attract and the contact abilities (2026-10-03, on Ian's yes).**
Every Pokemon now has a gender. A trainer's is the game's: the gender its
trainer file names, or else the personality's low byte the engine builds
(120 for a female trainer class, 136 for a male one, the lowest bit set by
an ability-slot request) against the species' ratio
(`fightsim.trainer_gender`, read from `res/trainers/data` by
`plscore.with_genders`, since the balance track's trainer data does not
carry it). A box member's is rolled once from a fixed seed by its catch and
kept in goal 2's records, the species at the fight deciding it as the game
does; a record without one is rolled from itself the same way. Attract
infatuates only across genders, not on Oblivious (unless Mold Breaker) or a
genderless Pokemon; love stops half the moves its holder tries and ends
when its object leaves. Building Cute Charm showed that no ability striking
back at a contact move was simulated at all, so Static, Poison Point, Flame
Body, Effect Spore (not on Grass types, Overcoat or Safety Goggles) and Cute
Charm now take 3 contact hits in 10, and Rough Skin and Oxide's Iron Barbs
an eighth of the attacker's HP, each only when the move did damage, as the
decomp's on-hit switch has them. The stress test rolls the love check twice
against the player, as it does full paralysis. Four checks in `test_plfixes`
(56 of 56 pass); the AI's own Attract and Captivate checks, which read
genders, are now live.

**Wish, Spite and Recycle (2026-10-03).** Wish (Lucas and Dawn 3's
Umbreon) heals whoever stands in its side's slot by half that Pokemon's
maximum HP at the second turn's end, and fails while one is pending
(FIELD_COND_CHECK_STATE_WISH). Spite (Spiritomb at Spear Pillar) takes 4 PP
from the target's last move, or what it has left (BtlCmd_TrySpite).
Recycle (Bronzong at Spear Pillar) brings back the item its user last used
up, if it holds nothing (BtlCmd_TryRecycle); every place the simulator
uses up an item (berries, Focus Sash, Power Herb, Natural Gift and Fling)
now keeps it for Recycle, while Knock Off and Thief take it for good. The
engine keeps the recyclable item per battle position, so a Pokemon could
recycle what the one before it used; here each Pokemon keeps its own. Two
checks in `test_plfixes` (58 of 58 pass).

**Held items, abilities and move effects (2026-10-03, on Ian's word via
the Overseer).** A sweep of every item, ability and move effect the
trainers use in the 33 story fights and in Kaizo's bosses of its first
three splits found those the simulator never applied. The ones acting
only through damage (type boosters, Expert Belt, Muscle Band, Choice
items, Technician, Thick Fat, Solid Rock and the like) are in the
calculator's rows already; the ones that change a fight as it runs are now
simulated as the decomp has them, in both simulators:

- the calculator's rows are made once per fight at full HP with each
  Pokemon's starting item, so `fightsim.state_mult` now adds what they
  cannot know: Torrent, Blaze, Overgrow and Swarm at a third of HP or less;
  a resist berry used up after the hit it halves (17 berries; the row's
  halving is undone once it is gone); Flail and Reversal by the HP bar's
  pixels; Water Spout by HP; Earthquake and Magnitude into Dig, Surf and
  Whirlpool into Dive, at double damage;
- berries: the status-curing ones (Pecha, Cheri, Chesto, Rawst, Aspear, and
  Lum) cure at once, Rest included; Berry Juice heals 20; Custap puts its
  holder first at a quarter of its HP (half with Gluttony); Gluttony eats a
  pinch berry at half;
- items: White Herb undoes lowered stages once; Wide Lens 1.1 accuracy;
  Toxic and Flame Orb at the turn's end; Shell Bell an eighth of the damage
  dealt;
- abilities: Aftermath (a contact KO costs the attacker a quarter, unless
  Damp); Unburden (Speed doubled once its item is gone, if it came in
  holding one); Truant; Natural Cure and Oxide's Regenerator on the way
  out; Speed Boost; Poison Heal; Heatproof's halved burn; Inner Focus;
  Synchronize (Oxide passes bad poison on as bad poison); Magnet Pull,
  Shadow Tag and Arena Trap in the player's options (the trainer's AI had
  them); Unaware; Super Luck's crit stage;
- moves: Rage; Last Resort; Hurricane as Thunder in rain and sun (Oxide),
  with its confusion.

Five grouped checks in `test_plfixes` (63 of 63 pass). Multi-hit moves
still count as three hits, Secret Power's secondary effect needs the
terrain as Camouflage does, and Baton Pass still passes nothing.

Still not simulated: **Camouflage** (Barry 3's Staryu, the only user). It
changes its user's types to the battle's terrain type, and the simulator's
damage comes from calculator rows made once per fight with each Pokemon's
own types, so it needs rows for the changed type (as Magnitude has rows per
power) and the terrain of Barry 3's map. It matters first at Barry 3, in
goal 3. The damage model
still counts a two-to-five-hit move as three hits, and Baton Pass passes
nothing.

**For Ian: the player's genders.** Attract and Cute Charm work only between
Pokemon of opposite genders. A trainer's Pokemon have fixed genders in the
game: each member's personality, which carries its gender, is built from
its IV scale, level and species, the trainer's ID and class, and its
ability field, and Oxide's trainer files may name a gender outright
(`TrainerMon_Personality` in `src/trainer_data.c`), so those can be
computed. The box's
genders are not in goal 2's records. The proposal: roll each box member's
gender once from a fixed seed by its species' ratio, as the box's natures
were rolled, and keep it in the box's records. Jupiter 1 is read again once
that is settled.

## Ian's answers (2026-10-03, relayed by the Overseer)

1. Budget 64 for the play-out planner, in the check and every play-out
   reading from now on, with finalists whose win rates lie within five
   points counted as equal before faints decide (`plplan.BUDGET`,
   `plteam.WIN_TOL`).
2. Goal 2's four lines are good enough, and goal 2 is passed. Jupiter 1 is
   read again once Attract works.
3. Genders: each box member's rolled once from a fixed seed by its species'
   ratio and kept in the box's records, the trainers' computed from their
   personality, then Attract and Cute Charm; Wish, Spite, Recycle and
   Camouflage go in too.
4. The loop is approved as built: the rebuilt sixes go straight to the
   play-out check.
5. The boss-wide network is parked as a note in the tracker's Backlog.
6. Goal 3 waits until the Overseer has settled with Ian how it runs beside
   the Kaizo study, whose worked examples will want the scorer's readings.
   For that study, `docs/oxide/how-a-fight-is-read.md` describes a reading
   in plain words.

## Goal 2's readings (2026-10-03, for Ian to read)

The team search has read goal 2's four fights that have no hand-played
line, on goal 2's boxes (`plgoal2.py`): every member at the fight's cap
with its whole move pool from its catch, the trainer's team a Piplup player
meets, and the boosters reachable by then. Each fight passes when Ian has
read its line and accepts it. Barry 2 and Lucas and Dawn 2 are won cleanly
every time, Jupiter 1 nearly so, and Fantina is by far the hardest fight
read yet: won about 19 times in 20, losing two or three Pokemon a fight.

Ian's standard reading of each winner, by the play-out planner (75 fights
at real odds, 25 very unlucky):

| Fight | Cap | The winner | Real odds | Very unlucky | Search, minutes |
|---|---|---|---|---|---|
| Barry 2 | 11 | Piplup, Vulpix, Rookidee, Dottler, Starly, Krabby | 100% won, 0.00 faints, 100% clean | 100%, 0.00, 100% | 12 |
| Jupiter 1 | 27 | Dubwool, Vulpix, Onix, Tsareena, Graveler, Snover | 100%, 0.07, 93% | 100%, 0.32, 72% | 59 |
| Lucas and Dawn 2 | 30 | Prinplup, Dubwool, Vulpix, Whiscash, Kingler, Tsareena | 100%, 0.00, 100% | 100%, 0.00, 100% | 21 |
| Fantina | 33 | Vulpix, Tsareena, Graveler, Ampharos, Vikavolt, Rampardos | 94.7%, 2.21, 12% | 88%, 3.32, 4% | 57, then the loop |

**Barry 2** ([line](../../tools/oxide/balance/perfectline_results/step3/goal2-barry_2-line.txt)):
Vulpix leads and Embers Starly and then Turtwig through its Withdraw, four
turns, nothing hurt. At the cap of 11 the fight is a formality for any of
the three finalists, as it was at 16.

**Jupiter 1** ([line](../../tools/oxide/balance/perfectline_results/step3/goal2-jupiter_1-line.txt)):
Graveler takes Delcatty's Fake Out and chips it; Onix, put to sleep by
Sing as it switches in, gives way to Dubwool, whose Double Kick finishes
Delcatty; the sleeping Onix comes back in to take Sableye's Fake Out, and
again later to take Skuntank's Screech; Graveler's Rock Blast wears
Sableye down through its Shadow Sneaks;
Tsareena's Trop Kick and Stomp take Skuntank, with switches to Onix and
Graveler to spread its Night Slashes; Snover's Icy Wind ends Tangela. No
rule names any of this: switching a sleeping Pokemon in to absorb hits, and
spreading damage by switching, arose from the search. The network read
this six at 93% won and 0.69 faints, the play-outs at 100% and 0.07; it was
third of three on the network and first on the check. **Caveat:**
Delcatty's Attract and Cute Charm do nothing in the simulator (genders,
above), and its Attract came three times in this line, so the reading is
kinder than the fight. It is read again once the genders are settled.

**Lucas and Dawn 2** ([line](../../tools/oxide/balance/perfectline_results/step3/goal2-lucas_dawn_2-line.txt)),
read on the fixed simulator: Dubwool Growls Lopunny and wears it down;
Whiscash takes over, sets Amnesia against Jynx and sleeps through Lovely
Kiss; its Magnitude takes Monferno; against Jolteon, Magnet Rise now makes
Magnitude fail, and Whiscash finishes it with Water Pulse. The first reading,
on the simulator without Magnet Rise and Torment, also won every fight
cleanly.

**Fantina** ([line](../../tools/oxide/balance/perfectline_results/step3/goal2-fantina-line.txt)),
on the simulator with Pain Split: the hardest fight read yet. The search's
own winner (Prinplup, Vulpix, Kingler, Tsareena, Ampharos, Rampardos) won
24 of 25 check fights but lost 4.2 Pokemon a fight. Its race had run on a
network that read the finalists at 24 to 43% won against the play-outs' 80
to 96%, and had settled on a core with Prinplup and Kingler, whose screen
margins against Mismagius, Rotom and Sableye, the enemies that caused the
faints, were among the box's worst. Two sixes built by hand from those
margins won every fight with 2.8 faints, so the search now has a loop
(below) that does this itself. On Fantina it read four sixes:

| Six | Won | Faints | Clean |
|---|---|---|---|
| the search's winner: Prinplup, Vulpix, Kingler, Tsareena, Ampharos, Rampardos | 96% | 4.20 | 0% |
| round 1, the six answering the faint-causers best: Tsareena, Graveler, Ampharos, Vikavolt, Rotom, Rampardos | 100% | 2.80 | 0% |
| round 1, the winner with Prinplup and Kingler swapped for Graveler and Vikavolt | 100% | 2.40 | 4% |
| round 2: Tsareena, Ampharos, Golbat, Vikavolt, Rotom, Rampardos | 96% | 2.40 | 0% |

The loop's winner, Vulpix, Tsareena, Graveler, Ampharos, Vikavolt,
Rampardos, is the table's above. Its faints fall to Mismagius (76 of 166 in
the 75 real fights), Rotom (46), Sableye (27) and Drifblim (17). In the line
Vulpix burns Duskull and Flamethrowers it to its last HP; Ampharos
paralyses Drifblim and Discharges through its Calm Minds; against
Mismagius the planner paralyses it, then switches through Graveler,
Ampharos, Vikavolt and Rampardos to spread its Shadow Balls until
Rampardos's Assurance takes it in one hit; Rampardos and Tsareena wear
Sableye down through its Recovers; Tsareena's Trop Kick ends Rotom. That
seed is a lucky one (nothing faints); 2.2 faints is the average. Fantina
at 33 is a fight goal 2's box wins almost always but rarely without
losses, harder than Gardenia; whether that is the difficulty Ian wants for
his third gym is his call and the trainer pass's.

**The loop.** `plteam.improve` is Ian's diagnose-and-loop, with one
departure for his check: the enemies the best six's faints fell to,
weighted by count, pick the members that answer them by the screen's
margins, and two sixes built from those (the six answering them best, and
the best six with its two weakest answerers swapped for the two strongest
it lacks) go straight to the play-out check, rather than raising the race's
member weights and racing again on a network that misreads hard fights.
The best by Ian's order is kept, up to three rounds, stopping when nothing
beats it. It costs nothing where the winner loses no Pokemon, and at most
six more 25-fight readings where it does; at Fantina it read three more
sixes, about 6 core-hours. It ran here on the finished search; from now on
`plteam.search` runs it after the check.

## The Kaizo study's worked examples (2026-10-03, for the study)

The Kaizo study rebuilt five of Oxide's trainers at 6/10 of Kaizo and asked
for a reading of each (`~/oxide-trials/kaizo-teams/out/examples.md`).
`plstudy.py` reads the files where they lie, without copying them into
`res/`, and writes each reading to `~/oxide-trials/scorer-stage2/study/`.
Numbers are won / faints / clean, over 75 fights at real odds and 25 very
unlucky:

| Example | Real odds | Very unlucky | The study expected |
|---|---|---|---|
| Taylor, blind at 19 | 97 / 0.48 / 80 | 96 / 0.56 / 80 | 100 / 0.05 / 95 |
| Taylor, the box without its level-6 Starly | 100 / 0.13 / 91 | 92 / 0.72 / 72 | |
| Catherine, blind at 33 | 95 / 0.89 / 63 | 88 / 1.68 / 36 | 100 / 0.15 / 85 |
| Catherine, without the Starly | 99 / 0.55 / 67 | 92 / 1.52 / 52 | |
| the Eterna 1F grunt alone, blind at 27 | 100 / 0.00 / 100 | 100 / 0.00 / 100 | 100 / 0.03 / 97 |
| Eterna 1F and 2F, four grunts as one section | 100 / 0.01 / 99 | 100 / 0.08 / 92 | 80 clean or better |
| Gardenia, team search at 26 | 100 / 0.05 / 95 | 100 / 0.08 / 92 | 99 to 100 / 0.6 / 45 |
| Maylene, team search at 38, on a stand-in box | 99 / 2.75 / 0 | 96 / 3.32 / 0 | 98 to 99 / 1.0 / 30 |

A blind reading draws its own six at random from the whole box for each of
its 100 fights, as a player meeting the trainer with no plan might bring any
six they own. That is harsher than a settled six, and a box with fodder in
it shows it. The hand run's box at 19 (Taylor's) and goal 2's Fantina box at
33 (Catherine's) both keep a level-6 Starly, which three of Taylor's draws in
eight carried and one of Catherine's in five, so each is read again without
it. Taylor then sits in the study's band, her faints falling to Tangela.
Catherine still reads harder than expected, her faints falling to Haunter
(23 of 41), Drifblim and Litwick. The very unlucky column is 25 fights, each
with its own six, so it moves several points from one draw to the next.

The section carries one random six through all four grunts, with its HP,
status, PP and items as each fight left them, and stops at a loss; a run is
clean only when nothing faints in any of the four. The grunt and the section
use goal 2's Jupiter 1 box at 27. Gardenia's search, on the hand run's
Gardenia box at 26, chose Dubwool, Vullaby, Krabby, Charmeleon, Tsareena and
Breloom, which lost a Pokemon in 4 fights of 75.

Maylene's box is a stand-in: goal 2's Fantina box raised to 38, with the
level evolutions that brings (Empoleon, Staraptor, Blastoise, Charizard,
Primarina, Talonflame, Glimmora, Skuntank) and no moves beyond those its
pools reach by 38. No run has reached Maylene, so it says what Fantina's box
would face there, not what a player would bring. Its six, Staraptor,
Tsareena, Graveler, Primarina, Rotom and Talonflame, loses its Pokemon to
Medicham (92 of 206 faints), Hitmonchan (43), Lucario (28) and Toxicroak
(23). In the search's matchup table, Pure Power Medicham and Iron Fist
Hitmonchan with an Expert Belt each take 89 to 118 percent of the HP of every
member of that six but Rotom in one hit; Medicham outspeeds four of the six,
and its Coba Berry halves the Flying members' hits. The Twins are a double
and are not read.

The trainer file's ability field is read as the build reads it: 0 gives the
first slot (the class's default personality byte is even), 1 and 2 the
slots, and 3 the hidden one. Taylor's first member names no item, and the
trainer packer keeps a party's items only when its first member names one,
so the built game would drop Tangela's Sitrus Berry; the reading gives
Cherubi "ITEM_NONE" so that the berry stays, as the study means it, and
records the note.

**A second effect sweep.** The examples brought moves and abilities the
simulator did not apply, and a stricter pass over the 33 story fights and
Kaizo's six, by effect alone (the first sweep had passed over any move whose
name the source mentioned), found Gyro Ball in Mars 2, Mars and Jupiter, and
Saturn 2. Each is now as the decomp has it, with a check in `test_plfixes`
(70 of 70 pass). Hex and Infernal Parade double on a target with a status,
and Venoshock and Barb Barrage on a poisoned one, in the hit and not in the
trainer AI's figure, which scores them through Expert_Hex. Assurance doubles
on a target that lost HP earlier in the turn, but not for hazards on a
knockout's replacement, which the game counts after the turn's flags clear.
Mortal Spin poisons its target, and Rapid Spin raises its user's Speed
(Oxide); both free the user from binding and Leech Seed and clear its
side's hazards. Corrosion poisons Poison and Steel types with its holder's
moves, never through an ability, a hazard or an Orb. Poison Touch poisons 3
times in 10 on a contact hit, when the defender's own on-hit ability did
nothing. Gust and Twister reach a Pokemon in the air at double damage, and
Thunder, Sky Uppercut, Hurricane and Smack Down at their power (Smack
Down's grounding is not simulated). Gyro Ball's power follows the turn's
Speeds, as the trainer's AI already reckoned it. Catherine (Hex), the
section (Assurance) and Maylene (Mortal Spin, Venoshock, Corrosion, Poison
Touch) were read again on the fixed simulator; their first readings stay
beside them as `-oldsim`. Maylene's first, with a weaker six, was 91 / 3.03
/ 7, very unlucky 84 / 3.92 / 0.

## Goal 2 read again on the fixed simulator (2026-10-03)

The simulator changed under goal 2's readings: genders, Attract and Cute
Charm, the contact abilities, Wish, Spite and Recycle, the battle-state
sweep, and the study's second sweep all went in on 2026-10-03. Each of goal
2's four fights, and the three gyms of the team search's first test, was
searched and read again: budget 64, the five-point tolerance, the loop, and
Ian's standard reading of the winner. Jupiter 1's re-read and Fantina's
search ran before the second sweep, which reaches them only through the
box's Rapid Spin and Assurance; the rest ran after it. Numbers are won /
faints / clean.

| Fight | Before: six | Real | Very unlucky | After: six | Real | Very unlucky |
|---|---|---|---|---|---|---|
| Barry 2 | Piplup, Vulpix, Rookidee, Dottler, Starly, Krabby | 100 / 0.00 / 100 | 100 / 0.00 / 100 | Wooloo, Vulpix, Rookidee, Dottler, Starly, Krabby | 100 / 0.00 / 100 | 100 / 0.00 / 100 |
| Jupiter 1 | Dubwool, Vulpix, Onix, Tsareena, Graveler, Snover | 100 / 0.07 / 93 | 100 / 0.32 / 72 | Dubwool, Onix, Graveler, Breloom, Vikavolt, Rotom | 100 / 0.19 / 91 | 100 / 0.20 / 88 |
| Lucas and Dawn 2 | Prinplup, Dubwool, Vulpix, Whiscash, Kingler, Tsareena | 100 / 0.00 / 100 | 100 / 0.00 / 100 | Prinplup, Vulpix, Whiscash, Wartortle, Onix, Tsareena | 100 / 0.00 / 100 | 100 / 0.00 / 100 |
| Fantina | Vulpix, Tsareena, Graveler, Ampharos, Vikavolt, Rampardos | 95 / 2.21 / 12 | 88 / 3.32 / 4 | Charmeleon, Tsareena, Graveler, Ampharos, Vikavolt, Rampardos | 91 / 3.04 / 1 | 76 / 3.92 / 0 |
| Fantina, the same six as before | | | | Vulpix, Tsareena, Graveler, Ampharos, Vikavolt, Rampardos | 92 / 2.89 / 4 | 92 / 3.00 / 8 |
| Roark, at 16 | Wooloo, Barboach, Nidorino, Onix, Charmander, Geodude | 100 / 0.12 / 88 (25 play-outs) | | Barboach, Nidorino, Onix, Charmander, Steenee, Geodude | 100 / 0.05 / 95 | 100 / 0.16 / 84 |
| Mars 1, at 19 | Prinplup, Bibarel, Vullaby, Onix, Charmander, Geodude | 100 / 0.00 / 100 (25 play-outs) | | Prinplup, Bibarel, Nidorino, Onix, Charmander, Geodude | 100 / 0.16 / 87 | 96 / 0.56 / 76 |
| Gardenia, at 26 | Dubwool, Bibarel, Vullaby, Charmeleon, Tsareena, Golbat | 96 / 1.52 / 16 (25 play-outs) | | Dubwool, Bibarel, Nidorino, Onix, Tsareena, Golbat | 97 / 1.07 / 44 | 88 / 2.00 / 24 |

Barry 2 and Lucas and Dawn 2 stay clean every time. Jupiter 1, now with
Attract working, loses a Pokemon in about one fight in eleven, as before,
its faints still falling to Skuntank. Fantina is the one the fixes moved: the
same six loses 2.89 Pokemon a fight where it lost 2.21, and wins cleanly 4
percent of the time where it did 12. Drifblim causes most of the difference: its
faints rose from 17 to 41 in the 75 real fights, because Unburden now
doubles its Speed once its Sitrus Berry is eaten. The re-read's search
chose a six with Charmeleon for Vulpix that reads no better than the old
one (its 25-fight check put it at 100 / 2.52 / 0); within the search's
check, sixes this close are not told apart. The three gyms' "before" figures
are their first test's 25-fight checks rather than full readings, so a 0.16
average can show as none.

Gardenia, at 97 / 1.07 / 44, reads kinder than its first test's 25-fight
check of another six; Roserade still causes 60 of its 80 faints. The new
lines are beside the old ones in `perfectline_results/step3/`
(`goal2-<fight>-line-reread.txt`), and every number here is in
`readings-2026-10-03.json` there. In Fantina's new line the planner brings
Charmeleon in on Duskull's opening Will-O-Wisp, which cannot burn a Fire
type; no rule names that.

## The Kaizo anchor (2026-10-03, on Ian's yes)

Kaizo's six readable bosses of its first three splits, read on goal 2's
boxes with the team search at budget 64 and the loop, as goal 2's fights
are (`plstudy.py`, `kaizo_*`). Mars is a double and is left out, as the
Overseer agreed. Each Kaizo team is the variant a Piplup player meets, with
its levels carried onto Oxide's split the same distance under the cap
(Kaizo's caps of 16, 28 and 38 against Oxide's 16, 26 and 33). Barry 2 and
Jupiter are mini-bosses with no cap of their own in Kaizo, so their ace
goes to Oxide's interim cap at that fight (11 and 27) and the rest follow
it; by Kaizo's split cap they would sit far under the box. Kaizo's weathers
stay (Roark's sand, Gardenia's rain). Beside each is Oxide's own reading of
the same fight on the same box, from goal 2's re-reads.

| Kaizo boss | Cap | Kaizo's team on Oxide's levels | The search's six | Real odds | Very unlucky | Oxide's same fight, real odds |
|---|---|---|---|---|---|---|
| Barry 2 | 11 | Aipom 10, Taillow 10, Slakoth 10, Mankey 10, Elekid 10, Turtwig 11 | Piplup, Vulpix, Rookidee, Squirtle, Krabby, Finneon | 0 / 6.00 / 0 | 0 / 6.00 / 0 | 100 / 0.00 / 100 |
| Roark | 16 | Bonsly 15, Lileep 13, Gible 14, Corsola 14, Shuckle 13, Cranidos 16 | Wartortle, Nidorino, Onix, Charmander, Steenee, Geodude | 81 / 4.31 / 0 | 68 / 4.72 / 0 | 100 / 0.05 / 95 |
| Gardenia | 26 | Miltank 24, Rotom-Mow 23, Ludicolo 22, Milotic 23, Roserade 24, Torterra 26 | Dubwool, Tsareena, Graveler, Vikavolt, Breloom, Golbat | 24 / 5.36 / 1 | 24 / 5.48 / 0 | 97 / 1.07 / 44 |
| Jupiter | 27 | Skuntank 27, Electrode 26, Gyarados 25, Medicham 25, Lunatone 25, Tangrowth 26 | Dubwool, Charmeleon, Tsareena, Graveler, Golbat, Rotom | 80 / 4.17 / 0 | 44 / 5.32 / 0 | 100 / 0.19 / 91 |
| Fantina's second team | 33 | Dusclops 26, Drifblim 27, Shedinja 28, Sableye 27, Banette 27, Mismagius 29 | Graveler, Ampharos, Rotom, Carbink, Rampardos, Eevee | 100 / 0.11 / 92 | 100 / 0.36 / 72 | |
| Fantina | 33 | Froslass 32, Drifblim 32, Gengar 31, Spiritomb 31, Rotom-Fan 32, Mismagius 33 | Tsareena, Graveler, Ampharos, Pawmo, Vikavolt, Rampardos | 40 / 4.56 / 11 | 40 / 4.56 / 0 | 91 / 3.04 / 1 |

On the same boxes, Oxide's bosses are won 91 to 100 times in 100, and
Kaizo's 0 to 81 times, its second Fantina team aside. Kaizo's cost four to
six Pokemon a fight where Oxide's cost at most three. Barry 2 is the
starkest. Each of Kaizo's six but Slakoth and Turtwig outspeeds every member
of the box, and one of their hits takes 40 to 100 percent of a member's HP
while the box's best take 10 to 56 percent of theirs. Elekid's Expert Belt
Shock Wave knocks out Rookidee and Krabby in one hit, and the box is ten
unevolved Pokemon still on Pound, Tackle and Bubble. Kaizo's second Fantina
team, four to seven levels under the cap, is the one fight the box wins
easily. The readings anchor the study's dial at Kaizo's full strength;
Kaizo's teams were built against Kaizo's own encounters, and are read here
against Oxide's box.

The reader could not carry three things over. Kaizo's Mankey has Reckless,
an ability Oxide's Mankey cannot have, so it was read with its own first
ability. Kaizo's Gengar has Shadow Tag; it was read with Levitate.
Gardenia's "Water Ball" names no move, and was dropped. Taillow's Secret
Power deals its damage, but its secondary effect waits on the terrain, as
Camouflage does (the list the Overseer had before the readings). Each
reading took 52 to 98 minutes on twelve workers. Kaizo's Fantina first
stopped partway: Sleep Talk drew its move outside the play-outs' dice, so
two replays of one turn could differ. It now draws through them, and no
earlier reading had a Pokemon talking in its sleep.

## Ian's answers (2026-10-04, relayed by the Overseer)

1. An ordinary trainer is read blind from a random six of the box's
   stronger half, never a member held below the cap. The targets: an
   ordinary trainer won cleanly 80 to 85 percent of the time; no boss above
   95 percent won; the hardest bosses near the easiest of Kaizo's on our box
   (about 80 percent won). The numbers order fights; they do not measure
   them absolutely.
2. The Jubilife grunts' tag battle belongs to Gardenia's split, as the game
   scripts it.
3. Trainers may use TM and tutor moves freely.

**What changed.** `plteam.blind_pool` gives the members a blind six is
drawn from, in both the study's reader and the perfect-line scorer: the
members at the cap, ranked by `plteam.split_strength`, and the top half of
them, six at least. A member's strength is its mean margin against every
Pokemon of the split's ordinary singles trainers, as the screen reckons
margins (hits it needs against hits it takes, half a hit for moving first,
clipped to 3 either way), with its own moves; the trainer being read is
left out of that panel, so the reading stays blind. A first try ranked by
stats and the best attack alone put Onix and Bibarel at the top of the hand
run's box at 19 and left Vulpix and Charmander out, against a split of
Grass trainers; the margins keep both, as a player would. Ranked so, the
blind examples keep 8 of Taylor's 16, 15 of Catherine's 31 and 12 of the
grunt's 24, and the level-6 Starly is out of all three; a check in
`test_plfixes` (72 of 72) holds the rule. The Jubilife pair (trainers 414
and 415) joins `plscore.SPLIT_OVERRIDE`: Jubilife is first reached before
Roark, so `splits.trainer_split` puts them in his split, but the Oreburgh
Gym's win sets VAR_JUBILIFE_CITY_STATE to 3, at which Jubilife's script
starts the battle; `trainers.csv` now has the pair first in Gardenia's
split. No reader of this track checks a trainer's moves for legality, so
TM and tutor moves already pass. Ian accepted this definition of the
stronger half for now (2026-10-06, relayed by the Overseer), to be adjusted
if it keeps landing on bad boxes.

The study's four blind examples read again with the stronger half (won /
faints / clean; the earlier readings stay beside them as `-olddraw`):

| Example | Real odds | Very unlucky | Before, real odds |
|---|---|---|---|
| Taylor, at 19 | 100 / 0.00 / 100 | 100 / 0.00 / 100 | 97 / 0.48 / 80 |
| Catherine, at 33 | 100 / 0.27 / 83 | 100 / 0.28 / 84 | 95 / 0.89 / 63 |
| the Eterna 1F grunt, at 27 | 100 / 0.00 / 100 | 100 / 0.00 / 100 | 100 / 0.00 / 100 |
| the Eterna section, at 27 | 100 / 0.00 / 100 | 100 / 0.00 / 100 | 100 / 0.01 / 99 |

Catherine now sits in Ian's 80 to 85 band; Taylor and the Eterna grunts
read trivial. The first try at the new draw hung on Taylor: it asked for
75 different sixes from a pool of eight, which makes 28, so each fight now
draws its own six and may repeat one.

## The Kaizo study's comb of Roark's split (2026-10-06, for Ian's check)

The study rebuilt Roark's split (`~/oxide-trials/kaizo-teams/out/comb/`,
reported in its `roark.md`), and its expectations came from its own rough
simulator, so the Overseer set three checks for the scorer's readings in
their place: Roark, by the team search at 16 on the three-gym run's Roark
box, 95 percent won or below; Barry 2, by the team search at 11 on goal 2's
Barry 2 box (a Piplup player's file), 95 percent won or below; every other
trainer but the Jubilife tag pair blind from the stronger half, at 11
before Barry 2 and 16 after, 80 to 85 percent clean. `plstudy.py`'s
`comb_*` entries read them from the study's files. Numbers are won /
faints / clean; one of eighteen passes.

| Trainer | Path | At | The study expected | Real odds | Very unlucky | Check |
|---|---|---|---|---|---|---|
| Youngster Tristan | required | 11 | 100 / 0.10 / 89 | 100 / 0.00 / 100 | 100 / 0.08 / 92 | fail, too easy |
| Youngster Logan | required | 11 | 100 / 0.15 / 83 | 100 / 0.00 / 100 | 100 / 0.04 / 96 | fail, too easy |
| Lass Natalie | required | 11 | 100 / 0.15 / 81 | 100 / 0.03 / 97 | 100 / 0.20 / 88 | fail, too easy |
| School Kid Harrison | optional | 11 | 100 / 0.20 / 81 | 92 / 0.72 / 73 | 88 / 0.72 / 88 | fail, too hard |
| School Kid Christine | optional | 11 | 100 / 0.15 / 85 | 100 / 0.01 / 99 | 100 / 0.00 / 100 | fail, too easy |
| Barry 2 | required, boss | 11 | 93 / 3.0 / 0 | 100 / 2.72 / 0 | 92 / 2.76 / 0 | fail, over 95 won |
| Youngster Michael | optional | 16 | 100 / 0.20 / 90 | 96 / 0.49 / 79 | 100 / 0.16 / 88 | fail, too hard |
| Lass Madeline | optional | 16 | 100 / 0.15 / 84 | 100 / 0.20 / 87 | 96 / 0.60 / 72 | fail, too easy |
| Lass Kaitlin | optional | 16 | 100 / 0.15 / 85 | 100 / 0.15 / 87 | 100 / 0.20 / 84 | fail, too easy |
| Youngster Dallas | optional | 16 | 100 / 0.15 / 88 | 100 / 0.36 / 83 | 88 / 1.32 / 56 | pass |
| Youngster Sebastian | optional | 16 | 100 / 0.10 / 87 | 100 / 0.01 / 99 | 100 / 0.00 / 100 | fail, too easy |
| Camper Curtis | optional | 16 | 100 / 0.20 / 79 | 93 / 1.44 / 32 | 88 / 1.96 / 24 | fail, too hard |
| Picnicker Diana | optional | 16 | 100 / 0.25 / 82 | 100 / 0.35 / 75 | 100 / 0.36 / 80 | fail, too hard |
| Worker Colin | optional | 16 | 100 / 0.15 / 83 | 100 / 0.07 / 93 | 100 / 0.04 / 96 | fail, too easy |
| Worker Mason | optional | 16 | 100 / 0.10 / 90 | 100 / 0.11 / 89 | 100 / 0.00 / 100 | fail, too easy |
| Youngster Jonathon | optional | 16 | 100 / 0.15 / 77 | 100 / 0.15 / 87 | 100 / 0.36 / 84 | fail, too easy |
| Youngster Darius | optional | 16 | 100 / 0.15 / 84 | 100 / 0.57 / 65 | 96 / 0.72 / 64 | fail, too hard |
| Roark | required, boss | 16 | 90 / 2.3 / 5 | 99 / 1.91 / 4 | 92 / 2.48 / 0 | fail, over 95 won |

The two bosses land on the study's faints (Barry 2's Munchlax wall takes
146 of 204 Pokemon, Roark's Lileep 71 of 143) but are never lost at real odds;
Barry 2's six is Piplup, Wooloo, Vulpix, Rookidee, Dottler and Krabby,
Roark's Prinplup, Nidorino, Onix, Charmander, Steenee and Geodude.

**For Ian: the blind pool leans on one weakness.** Ranked against Roark's
split, whose trainers are mostly Rock types, the stronger half at 16 is
Prinplup, Bibarel, Barboach, Wartortle, Krabby, Finneon, Onix and Geodude:
all eight are weak to Grass, and Vulpix, Charmander, Corvisquire, Nidorino
and Steenee are out. Curtis's Roselia at 14 (Mega Drain, Stun Spore,
Growth) then makes 92 of his 108 faints, and Michael's Grass team and
Darius's Kabuto read hard for the same reason. At 11 the box keeps nine
members at the cap, so the half is the six-member floor, the same six in
every fight, four of them Water types; Harrison's Abra, with Charge Beam,
makes 45 of his 54 faints while the other four trainers there read
trivial. Ian accepted the stronger half "to be adjusted if it keeps landing
on bad boxes" (2026-10-06), and these are bad boxes. As a check: "a blind
pool has no weakness shared by more than half its members", verified by
the session on every reading's pool, fails today at both caps. One
adjustment: keep the stronger half, but swap its weakest members for the
strongest that resist the type most of the pool fears. His decision; a
re-read of the sixteen blind trainers then takes about 1.5 hours.

Ian keeps the rule as it is (2026-10-06, relayed by the Overseer): "Given
it's the first split of the game, I'm fine with it being a bit
biased/inaccurate with a skewed box here." No pool is adjusted for a shared
weakness, and the comb's readings above stand, every blind one drawn from
the stronger half.

Ian approved the comb as built (2026-10-06, relayed by the Overseer): the
teams are "all in the approximate right ballpark (barry and roark aren't
perfect, but I want to move on from the first split as I think it can
give funky data)". Roark's split is not read again; once he approves the
study's combs of Gardenia's and Fantina's splits, the three go into the
trainer files together and goal 3 reads those two splits' bosses (the
tracker's Scheduled list).

## Learnset checks 2 and 3 (2026-10-06, for the balance track's baseline)

Ian's plan of learnsets by check and verify (`docs/oxide/learnset-checks.md`)
gives this track checks 2 (a niche) and 3 (move use), both from the team
search's matchup screen alone. `plniche.py` runs the screen on goal 3's 39
kept boss fights (Ace Trainers and doubles left out), three rolled boxes
each, once with oxide's level-up lists and once with learnset v3's, which
live only in `docs/oxide/learnset-proposal.tsv` on `balance-learngen-v2`
(`plteam.mon_data` reads another set of lists when `OXIDE_LEARNSETS` names
one). The results, JSON and a summary, are in
`~/oxide-trials/learnset-baseline/`; the balance job folds them into its
report. The screen counts 38 lines taken by no boss of their window under
either set, leads rather than verdicts with the support-like marked, and
134 moves never picked under oxide's lists against 125 under v3's; v3
changes the screen's picture for 13 lines only. Two limits the report
names: a box over 30 members is cut first by summed margins (from
Maylene's split on, 11 to 50 members a box), which drops walls and support
lines before the screen sees them; and an early box is small enough that
the top five sixes hold most of it, so "taken" says little there and the
best six says more. Most never-picked attacks are outclassed in their
pools, since the screen takes one attack a type.

## The cost of labelling every boss (2026-10-02)

The Overseer counted about 110 fights in goal 3 that need labelled positions
of their own (8 leaders, the Elite Four and the Champion, about 11 rival and
6 Lucas and Dawn fights, 12 Galactic fights and about 68 Ace Trainers): at
the three full rounds the gyms had, roughly 90 hours of labelling, repeated
for every fight the trainer pass changes. Four levers were measured that
afternoon. Every network below is the average of two trained from scratch
by one recipe, and every reading is at real odds.

**What labelling costs.** From the shards' own records:

| Labelling | Core seconds per 1,000 positions |
|---|---|
| a boss by the play-out planner, budget 192 (the full rounds) | 72 to 122 |
| a boss at budget 64 | 54 |
| a round from the network's own play, one decision in five labelled | 52 |
| the Ace Trainers of Fantina's split, budget 192 | 51 |
| ordinary trainers of the first three splits | 8 |

A full round for one boss is about 10 core-hours (some 20 minutes on 29
workers); a tenth of a round, about 43,000 positions, is about one.

**1. Ace Trainers do not generalise like ordinary trainers.** The two Ace
Trainers of Fantina's split, Allen (280) and Catherine (284), were read on a
box no labels used, 100 fights each:

| Planner | Allen | Catherine |
|---|---|---|
| the play-out planner | 99 clean, 100 won, 0.01 faints | 100, 100, 0.00 |
| networks that never saw them | 22, 79, 2.96 | 73, 96, 0.49 |
| networks with 20,000 of their positions each | 67, 91, 0.90 | 81, 97, 0.45 |
| networks with about 106,000 each | 80, 94, 0.60 | 86, 100, 0.16 |

They belong with the bosses: unseen they read far worse than play-outs, and
even 106,000 positions of their own leave a gap. Those positions came from
the play-out planner's own fights, about nine fights per box, which lever 4
below suggests is the weak point.

**2. Fewer positions per boss.** Networks trained on everything except one
boss's positions, plus that boss's labels in four amounts, 500 fights each:

| The boss's labels | Positions | Mars 1 | Gardenia |
|---|---|---|---|
| none | 0 | 151 clean, 412 won, 2.30 faints | 0, 9, 5.96 |
| a tenth of a round | about 42,000 | 465, 500, 0.09 | 2, 379, 2.99 (seeds 3 and 4: 82, 364, 2.83) |
| a third of a round | about 138,000 | 462, 489, 0.20 | 1, 269, 4.33 (seeds 3 and 4: 12, 265, 4.10) |
| one round | about 414,000 | 452, 500, 0.13 | 1, 383, 3.71 |
| all three rounds | about 1.2 million | 480, 500, 0.06 | 1, 402, 3.70 |

At Mars 1, where the clean rate shows quality, a tenth of a round already
reads 93% clean with every fight won; the three rounds reach 96%, and the
last two of them were labelled from the network's own play, which lever 4
separates. Gardenia's column is not a curve of amount. A third reads worse
than a tenth with both pairs of seeds, yet the networks' value error on her
held-out positions is the same for both (2.0 to 2.2 on our six). The gap is
one matchup: the third's networks lose Charmeleon to Lumineon in 260 fights
of 500, against 110 for the tenth's, so which few positions a subset happens
to judge well decides her reading more than how many positions it holds.

**3. Fewer play-outs per label.** A third of a round of Gardenia labelled at
budget 64 instead of 192 cost 54 core seconds per 1,000 positions against
105, and read 0 clean, 351 won, 3.86 faints, against the budget-192 third's
269 won (which carries the Charmeleon misjudgement). On this one comparison
budget 64 halves the cost with no measured loss.

**4. Rounds from the network's own play: spread, not deep.** At Mars 1,
starting from the tenth's networks, a small round in which they played and
play-outs labelled every decision gave 70,000 positions from only 21 fights
(0.81 core-hours) and made the planner worse: 403 clean, 465 won, 0.58
faints. The same cost spread over more fights, labelling one decision in
five (`pldata --label-share 0.2`), gave 48,000 positions from 75 fights
(0.70 core-hours) and made it better than all three full rounds: 486 clean,
500 won, 0.028 faints. So the tenth of a round and one spread round, 1.67
core-hours, read Mars 1 as well as the 28 core-hours of the full rounds.

**5. A team change does not reuse its old labels.** On an in-memory change
to Gardenia's team (no game data written: Lumineon given Icy Wind and Attract
for Natural Gift and Swagger, Breloom Seed Bomb and Headbutt for Bullet Seed
and Stun Spore, both holding a Sitrus Berry), which made her much easier,
500 fights each:

| Labels | Clean | Won | Faints |
|---|---|---|---|
| the play-out planner (75 fights) | 39 of 75 | 75 of 75 | 0.71 |
| her old team's labels only | 1 | 348 | 4.10 |
| a third of a round on the new team | 133 | 463 | 1.90 |
| both | 124 | 433 | 2.21 |
| none | 0 | 9 | 5.96 |

The old labels keep the network playing the old fight, and adding them to new
ones helps nothing. A changed fight needs new labels, at the same cost as a
new one.

**6. The recipe failed its two checks.** At Gardenia, one spread round after
the tenth gave 334 won of 500 and two gave 299, against 429 for the full
rounds. At Mars 1 at its new cap of 19, the tenth of a round alone read our
six at 49 clean of 75, every fight won, 0.44 faints, close to the bar (67.1%
clean, 99.8% won, 0.42 faints); after one spread round it read 33 clean, 73
won, 0.80 faints (and 271 clean, 481 won, 0.75 faints over 500). The spread
round helped only at Mars 1 at its old level. The team search therefore
labels with the play-out planner alone, a tenth of a round across ten sixes,
and checks its finalists with play-outs ("The team search's first test").

**The estimate for goal 3, now replaced** by the team search's costs, which
the rerun at Roark revises. With the recipe that matched the full rounds at
Mars 1, a tenth of a round by the play-out planner and one spread round from
the network's own play, a fight costs about 1.7 core-hours of labelling.
For about 110 fights that is about 185 core-hours, some 6 to 7 hours on 29
workers, and about 5 with budget 64 in the first stage. Training is minutes,
and reading every fight on 100 simulated fights about half an hour. Each
fight the trainer pass changes costs its 1.7 core-hours again, about 4
minutes of the machine. Two cautions: the recipe has been measured on one
boss so far (Mars 1; its check at Gardenia is the next reading), and the
Ace Trainers, read over random boxes, may need their labels spread over more
boxes than a boss read on one planned six.

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

1. **Roark, relatively quickly, passing its tests** (passed 2026-10-02: the
   network planner over 2,000 fights, Ian's "close enough, pass"). The planner plays our
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

## Goal 3's fights, for Ian to prune (2026-10-02)

One row per fight goal 3 could label: the 33 story fights of `fights.json`,
every other trainer of a leader, Elite Four, Champion, rival, commander or
Galactic boss class, every Galactic Officer, and every trainer named or
classed Ace Trainer. A rival's three starter teams and Lucas and Dawn's six
slots are one row; two Ace Trainers met only together are one row, since a
double against two trainers is one fight (Ian, 2026-09-28). The split is
`fights.json`'s for a story fight and the scorer's own rule for the rest
(`plscore.SPLIT_OVERRIDE`, then `b6.placements`, then
`splits.trainer_split`). Post-game means every map that battles it is in
the Post split (Route 224, Victory Road's back room, the Battleground) or
its ace is above the League cap of 78. Rematch means a team whose file is
named a rematch, or Barry's Battleground teams. Double means the trainer's
own double flag, a tag fight in `fights.json`, or a map whose script gives
the player a partner (Riley on Iron Island B2F, Buck in Stark Mountain's
second room, Marley in Victory Road's back room), where the engine makes
every trainer battle a tag battle; the planner plays one Pokemon a side and
`pdoubles` is a separate first-version search, so none of these can be
labelled yet. Unreachable means no map battles it; not placed means it has
no split. Optional comes from the reach model behind `b6.placements` and
from the docs, which call the Battle Zone and Iron Island optional; gyms
and dungeons are not modelled, so their trainers read "path unknown".

Uncertain. The three tag story fights (Somnu and Moira, Mars and Jupiter at
Spear Pillar, Flint and Volkner) are major bosses proposed for a drop only
because the planner cannot read doubles; covering them means doubles
support first. Two Ace pairs face each other with no partner: Dennis and
Maya on Route 215 (both on the path) and Felix and Dana on Route 229. Seen
together they are one double, but each can be fought alone by talking to it
from outside both sight lines, so they are kept as singles. Barry 1 is
proposed for a drop on Ian's ruling that it does not count, and Lucas and
Dawn 1 on his ruling to ignore it as trivial. The eight officer rows
(Somnu, Moira, Hesperid and Argo, twice each) and Mars and Jupiter at
Stark Mountain are probably not in the Overseer's count of about 12
Galactic fights; they are kept as named Galactic fights. The rematches'
post-game reading comes from their levels (82 to 90), not from their
scripts' gates. Goal 3's wording does not name the Frontier Brains (optional
bosses since 2026-09-27, still drafts) or the partners' own fights (Cheryl,
Riley, Marley, Buck, Mira), so they have no rows.

Rows: 121. Kept: 79. Proposed drops: 42 (27 rematch, 8 double, 4 post-game, 1 does not count, 1 trivial, 1 unreachable; a row with several reasons is counted under its first).

Rows by kind:

| kind | kept | dropped |
|---|---|---|
| gym leaders, Elite Four and Champion | 13 | 1 |
| Barry | 5 | 2 |
| Lucas and Dawn | 2 | 1 |
| named Galactic fights | 18 | 2 |
| Ace Trainers | 41 | 21 |
| rematches and re-fights | 0 | 15 |

| fight | ids | split | maps | flags | proposed | reason |
|---|---|---|---|---|---|---|
| Barry 1 | 850, 851, 852 | Roark | route 201 | Ian ruled it does not count for deaths or a wipe (2026-10-02) | drop | does not count |
| Lucas and Dawn 1 | 787, 788, 789, 790, 791, 792 | Roark | route 202 | Ian ruled to ignore it as trivial (2026-10-02) | drop | trivial |
| Barry 2 | 247, 248, 249 | Roark | route 203 |  | keep |  |
| Roark | 246 | Roark | oreburgh city gym |  | keep |  |
| Mars 1 | 295 | Gardenia | valley windworks building |  | keep |  |
| Gardenia | 315 | Gardenia | eterna city gym |  | keep |  |
| Jupiter 1 | 406 | Fantina | team galactic eterna building 4f |  | keep |  |
| Lucas and Dawn 2 | 793, 794, 799, 800, 801, 802 | Fantina | route 207 | map first reached earlier; fought on a return visit | keep |  |
| Fantina | 318 | Fantina | hearthome city dp gym leader room, hearthome city gym leader room |  | keep |  |
| Barry 3 | 470, 471, 472 | Maylene | route 209 gate to hearthome city |  | keep |  |
| Maylene | 317 | Maylene | veilstone city gym |  | keep |  |
| Barry 4 | 473, 474, 475 | Wake | pastoria city |  | keep |  |
| Wake | 316 | Wake | pastoria city gym |  | keep |  |
| Cyrus 1 | 913 | Byron | celestic town cave |  | keep |  |
| Barry 5 | 476, 477, 478 | Byron | canalave city |  | keep |  |
| Byron | 250 | Byron | canalave city gym |  | keep |  |
| Saturn 1 | 408 | Candice | valor cavern |  | keep |  |
| Somnu and Moira | 420, 427 | Candice | lake verity | double against two trainers (fights.json: tag); map first reached earlier; fought on a return visit | drop | double |
| Mars 2 | 405 | Candice | lake verity | map first reached earlier; fought on a return visit | keep |  |
| Candice | 319 | Candice | snowpoint city gym |  | keep |  |
| Cyrus 2 | 403 | HQ | galactic hq 4f |  | keep |  |
| Saturn 2 | 409 | HQ | galactic hq control room | whole fight under Trick Room | keep |  |
| Mars and Jupiter | 528, 407 | Galactic | spear pillar | double against two trainers (fights.json: tag); Barry beside the player | drop | double |
| Cyrus 3 | 404 | Galactic | distortion world b7f |  | keep |  |
| Volkner | 320 | Volkner | sunyshore city gym room 3 |  | keep |  |
| Flint and Volkner | 921, 922 | Barry | fight area | double against two trainers (fights.json: tag); Barry beside the player; map first reached earlier; fought on a return visit | drop | double |
| Lucas and Dawn 3 | 779, 780, 781, 782, 783, 784 | Barry | battleground, victory road 1f | the same six slots are fought again at the Battleground after the League | keep |  |
| Barry 6 | 479, 480, 481 | Barry | pokemon league north pokecenter 1f |  | keep |  |
| Aaron | 261 | League | pokemon league aaron room |  | keep |  |
| Bertha | 262 | League | pokemon league bertha room |  | keep |  |
| Flint | 263 | League | pokemon league flint room |  | keep |  |
| Lucian | 264 | League | pokemon league lucian room |  | keep |  |
| Cynthia | 267 | League | pokemon league champion room |  | keep |  |
| Galactic Officer Somnu (galactic_grunt_valley_windworks_3) | 299 | Gardenia | valley windworks building | on the path (reach model: required) | keep |  |
| Galactic Officer Moira (galactic_grunt_team_galactic_eterna_building_3f) | 423 | Fantina | team galactic eterna building 3f | optional (reach model: avoidable) | keep |  |
| Galactic Officer Argo (galactic_grunt_celestic_town) | 416 | Byron | celestic town | path unknown (scripted, not on a crossing) | keep |  |
| Galactic Officer Hesperid (galactic_grunt_lake_valor_2) | 418 | Candice | lake valor drained | on the path (reach model: required) | keep |  |
| Galactic Officer Moira (galactic_grunt_mt_coronet_5f_1) | 520 | Galactic | mt coronet 5f | path unknown (dungeon not modelled) | keep |  |
| Galactic Officer Somnu (galactic_grunt_mt_coronet_5f_2) | 525 | Galactic | mt coronet 5f | path unknown (dungeon not modelled) | keep |  |
| Galactic Officer Hesperid (galactic_grunt_mt_coronet_6f) | 526 | Galactic | mt coronet 6f | path unknown (dungeon not modelled) | keep |  |
| Galactic Officer Argo (dummy_834) | 834 | Galactic | mt coronet 6f | path unknown (dungeon not modelled) | keep |  |
| Commander Mars (commander_mars_stark_mountain) | 926 | Galactic | stark mountain room 1 | the Battle Zone, optional; Jupiter (927) follows straight after, no heal between; path unknown (scripted, not on a crossing) | keep |  |
| Commander Jupiter (commander_jupiter_stark_mountain) | 927 | Galactic | stark mountain room 1 | the Battle Zone, optional; fought straight after Mars (926), no heal between; path unknown (scripted, not on a crossing) | keep |  |
| Ace Trainer Allen (ace 29) | 280 | Fantina | hearthome city dp gym trainer room 5, hearthome city gym trainer room 2 | path unknown (gym not modelled) | keep |  |
| Ace Trainer Catherine (ace 29) | 284 | Fantina | hearthome city dp gym trainer room 6, hearthome city gym trainer room 2 | path unknown (gym not modelled) | keep |  |
| Ace Trainer Dennis (ace 35) | 278 | Maylene | route 215 | sight crosses Ace Trainer Maya (287) on every tile it sees: a double against both when both see the player, a single when talked to from outside both lines; on the path (reach model: required) | keep |  |
| Ace Trainer Maya (ace 35) | 287 | Maylene | route 215 | sight crosses Ace Trainer Dennis (278) on every tile it sees: a double against both when both see the player, a single when talked to from outside both lines; on the path (reach model: required) | keep |  |
| Ace Trainer Krystal (ace 44) | 795 | Wake | route 214 | optional (reach model: avoidable) | keep |  |
| Ace Trainer Ernest (ace 41) | 66 | Byron | route 210 north | optional (reach model: avoidable) | keep |  |
| Ace Trainer Alyssa (ace 42) | 67 | Byron | route 210 north | on the path (reach model: required) | keep |  |
| Ace Trainer Jake (ace 46) | 170 | Byron | route 221 | optional (off the story path) | keep |  |
| Ace Trainer Shannon (ace 45) | 171 | Byron | route 221 | optional (off the story path) | keep |  |
| Ace Trainer Cesar (ace 51) | 279 | Byron | canalave city gym | path unknown (gym not modelled) | keep |  |
| Ace Trainer Breanna (ace 50) | 283 | Byron | canalave city gym | path unknown (gym not modelled) | keep |  |
| Ace Trainer Jonah and Brenda (ace 47) | 388, 392 | Byron | iron island b2f left room | tag battle beside Pkmn Trainer Riley (IRON_ISLAND_B2F_LEFT_ROOM's partner); Iron Island, an optional gauntlet; sight lines cross: met together as one tag battle; on the path (reach model: required) | drop | double |
| Ace Trainer Blake (ace 48) | 132 | Candice | route 216 | optional (reach model: avoidable) | keep |  |
| Ace Trainer Garrett (ace 47) | 133 | Candice | route 216 | optional (reach model: avoidable) | keep |  |
| Ace Trainer Laura (ace 50) | 134 | Candice | route 216 | on the path (reach model: required) | keep |  |
| Ace Trainer Maria (ace 47) | 135 | Candice | route 216 | optional (reach model: avoidable) | keep |  |
| Ace Trainer Dalton (ace 52) | 140 | Candice | route 217 | on the path (reach model: required) | keep |  |
| Ace Trainer Olivia (ace 52) | 141 | Candice | route 217 | on the path (reach model: required) | keep |  |
| Ace Trainer Sergio (ace 54) | 268 | Candice | snowpoint city gym | path unknown (gym not modelled) | keep |  |
| Ace Trainer Isaiah (ace 55) | 269 | Candice | snowpoint city gym | path unknown (gym not modelled) | keep |  |
| Ace Trainer Savannah (ace 54) | 270 | Candice | snowpoint city gym | path unknown (gym not modelled) | keep |  |
| Ace Trainer Alicia (ace 55) | 271 | Candice | snowpoint city gym | path unknown (gym not modelled) | keep |  |
| Ace Trainer Anton (ace 54) | 827 | Candice | snowpoint city gym | path unknown (gym not modelled) | keep |  |
| Ace Trainer Brenna (ace 54) | 828 | Candice | snowpoint city gym | path unknown (gym not modelled) | keep |  |
| Ace Trainer Rodolfo (ace 55) | 563 | Galactic | route 225 | the Battle Zone, optional; optional (off the story path) | keep |  |
| Ace Trainer Saul (ace 60) | 564 | Galactic | route 227 | the Battle Zone, optional; optional (off the story path) | keep |  |
| Ace Trainer Jose (ace 58) | 565 | Galactic | route 228 | the Battle Zone, optional; optional (off the story path) | keep |  |
| Ace Trainer Felix (ace 58) | 566 | Galactic | route 229 | the Battle Zone, optional; sight crosses Ace Trainer Dana (575) on 4 of its 8 sight tiles: a double against both when both see the player, a single when talked to from outside both lines; optional (off the story path) | keep |  |
| Ace Trainer Quinn (ace 55) | 567 | Galactic | route 225 | the Battle Zone, optional; optional (off the story path) | keep |  |
| Ace Trainer Graham (ace 56) | 568 | Galactic | route 226 | the Battle Zone, optional; optional (off the story path) | keep |  |
| Ace Trainer Keenan and Kassandra (ace 60) | 569, 579 | Galactic | stark mountain room 2 | tag battle beside Pkmn Trainer Buck (STARK_MOUNTAIN_ROOM_2's partner); the Battle Zone, optional; sight lines cross: met together as one tag battle; path unknown (dungeon not modelled) | drop | double |
| Ace Trainer Stefan and Jasmin (ace 60) | 570, 580 | Galactic | stark mountain room 2 | tag battle beside Pkmn Trainer Buck (STARK_MOUNTAIN_ROOM_2's partner); the Battle Zone, optional; sight lines cross: met together as one tag battle; path unknown (dungeon not modelled) | drop | double |
| Ace Trainer Skylar and Natasha (ace 60) | 571, 581 | Galactic | stark mountain room 2 | tag battle beside Pkmn Trainer Buck (STARK_MOUNTAIN_ROOM_2's partner); the Battle Zone, optional; sight lines cross: met together as one tag battle; path unknown (dungeon not modelled) | drop | double |
| Ace Trainer Abel and Monique (ace 60) | 572, 582 | Galactic | stark mountain room 2 | tag battle beside Pkmn Trainer Buck (STARK_MOUNTAIN_ROOM_2's partner); the Battle Zone, optional; sight lines cross: met together as one tag battle; path unknown (dungeon not modelled) | drop | double |
| Ace Trainer Deanna (ace 55) | 573 | Galactic | route 225 | the Battle Zone, optional; optional (off the story path) | keep |  |
| Ace Trainer Moira (ace 58) | 574 | Galactic | route 228 | the Battle Zone, optional; optional (off the story path) | keep |  |
| Ace Trainer Dana (ace 57) | 575 | Galactic | route 229 | the Battle Zone, optional; sight crosses Ace Trainer Felix (566) on every tile it sees: a double against both when both see the player, a single when talked to from outside both lines; optional (off the story path) | keep |  |
| Ace Trainer Mikayla (ace 58) | 576 | Galactic | route 227 | the Battle Zone, optional; optional (off the story path) | keep |  |
| Ace Trainer Meagan (ace 59) | 577 | Galactic | route 228 | the Battle Zone, optional; optional (off the story path) | keep |  |
| Ace Trainer Sandra (ace 56) | 578 | Galactic | route 229 | the Battle Zone, optional; optional (off the story path) | keep |  |
| Ace Trainer Zachery (ace 60) | 281 | Volkner | sunyshore city gym room 3 | path unknown (gym not modelled) | keep |  |
| Ace Trainer Destiny (ace 60) | 285 | Volkner | sunyshore city gym room 3 | path unknown (gym not modelled) | keep |  |
| Ace Trainer Omar (ace 63) | 224 | Barry | victory road 2f | path unknown (dungeon not modelled) | keep |  |
| Ace Trainer Henry (ace 63) | 225 | Barry | victory road b1f | path unknown (dungeon not modelled) | keep |  |
| Ace Trainer Mariah (ace 63) | 226 | Barry | victory road 1f | path unknown (dungeon not modelled) | keep |  |
| Ace Trainer Sydney (ace 63) | 227 | Barry | victory road 2f | path unknown (dungeon not modelled) | keep |  |
| Ace Trainer Ruben (ace 80) | 282 | Post | route 224 | route_224 is post-game; ace 80, above the League cap of 78 | drop | post-game |
| Ace Trainer Jamie (ace 84) | 286 | Post | route 224 | route_224 is post-game; ace 84, above the League cap of 78 | drop | post-game |
| Ace Trainer Micah and Brandi (ace 78) | 389, 393 | Post | victory road 1f room 2 | victory_road_1f_room_2 is post-game; tag battle beside Pkmn Trainer Marley (VICTORY_ROAD_1F_ROOM_2's partner); sight lines cross: met together as one tag battle | drop | post-game; double |
| Ace Trainer Arthur and Clarice (ace 78) | 390, 394 | Post | victory road 1f room 2 | victory_road_1f_room_2 is post-game; tag battle beside Pkmn Trainer Marley (VICTORY_ROAD_1F_ROOM_2's partner); sight lines cross: met together as one tag battle | drop | post-game; double |
| Ace Trainer Dalton (ace 54) | 648 | none | none | no map battles it; no split; Vs. Seeker rematch team | drop | rematch; unreachable; not placed |
| Ace Trainer Olivia (ace 56) | 649 | none | none | no map battles it; no split; Vs. Seeker rematch team | drop | rematch; unreachable; not placed |
| Ace Trainer Jake (ace 55) | 663 | none | none | no map battles it; no split; Vs. Seeker rematch team | drop | rematch; unreachable; not placed |
| Ace Trainer Dennis (ace 45) | 664 | none | none | no map battles it; no split; Vs. Seeker rematch team | drop | rematch; unreachable; not placed |
| Ace Trainer Dennis (ace 61) | 665 | none | none | no map battles it; no split; Vs. Seeker rematch team | drop | rematch; unreachable; not placed |
| Ace Trainer Rodolfo (ace 62) | 666 | none | none | no map battles it; no split; Vs. Seeker rematch team | drop | rematch; unreachable; not placed |
| Ace Trainer Saul (ace 63) | 667 | none | none | no map battles it; no split; Vs. Seeker rematch team | drop | rematch; unreachable; not placed |
| Ace Trainer Shannon (ace 56) | 668 | none | none | no map battles it; no split; Vs. Seeker rematch team | drop | rematch; unreachable; not placed |
| Ace Trainer Maya (ace 45) | 669 | none | none | no map battles it; no split; Vs. Seeker rematch team | drop | rematch; unreachable; not placed |
| Ace Trainer Maya (ace 61) | 670 | none | none | no map battles it; no split; Vs. Seeker rematch team | drop | rematch; unreachable; not placed |
| Ace Trainer Deanna (ace 62) | 671 | none | none | no map battles it; no split; Vs. Seeker rematch team | drop | rematch; unreachable; not placed |
| Ace Trainer Moira (ace 60) | 672 | none | none | no map battles it; no split; Vs. Seeker rematch team | drop | rematch; unreachable; not placed |
| Leader Roark (leader_roark_rematch) | 858 | Roark | oreburgh city gym | ace 82, above the League cap of 78; rematch team | drop | rematch; post-game |
| Leader Gardenia (leader_gardenia_rematch) | 857 | Gardenia | eterna city gym | ace 83, above the League cap of 78; rematch team | drop | rematch; post-game |
| Leader Fantina (leader_fantina_rematch) | 860 | Fantina | hearthome city gym leader room | ace 84, above the League cap of 78; rematch team | drop | rematch; post-game |
| Leader Maylene (leader_maylene_rematch) | 854 | Maylene | veilstone city gym | ace 85, above the League cap of 78; rematch team | drop | rematch; post-game |
| Leader Wake (leader_wake_rematch) | 859 | Wake | pastoria city gym | ace 86, above the League cap of 78; rematch team | drop | rematch; post-game |
| Leader Byron (leader_byron_rematch) | 856 | Byron | canalave city gym | ace 87, above the League cap of 78; rematch team | drop | rematch; post-game |
| Leader Candice (leader_candice_rematch) | 853 | Candice | snowpoint city gym | ace 88, above the League cap of 78; rematch team | drop | rematch; post-game |
| Leader Volkner (leader_volkner_rematch) | 855 | Volkner | sunyshore city gym room 3 | ace 89, above the League cap of 78; rematch team | drop | rematch; post-game |
| Elite Four Aaron (elite_four_aaron_rematch) | 866 | League | pokemon league aaron room | ace 84, above the League cap of 78; rematch team | drop | rematch; post-game |
| Elite Four Bertha (elite_four_bertha_rematch) | 867 | League | pokemon league bertha room | ace 85, above the League cap of 78; rematch team | drop | rematch; post-game |
| Elite Four Flint (elite_four_flint_rematch) | 868 | League | pokemon league flint room | ace 86, above the League cap of 78; rematch team | drop | rematch; post-game |
| Elite Four Lucian (elite_four_lucian_rematch) | 869 | League | pokemon league lucian room | ace 87, above the League cap of 78; rematch team | drop | rematch; post-game |
| Champion Cynthia (champion_cynthia_rematch) | 870 | League | pokemon league champion room | ace 90, above the League cap of 78; rematch team | drop | rematch; post-game |
| Pkmn Trainer Barry (rival_survival_area_1) | 837, 838, 839 | Post | battleground | battleground is post-game; a Battleground re-fight of Barry | drop | rematch; post-game |
| Pkmn Trainer Barry (rival_survival_area_2) | 871, 872, 873 | Post | battleground | battleground is post-game; ace 85, above the League cap of 78; a Battleground re-fight of Barry | drop | rematch; post-game |
| Pkmn Trainer Barry (rival_survival_area_unused) | 840, 841, 842 | none | none | no map battles it; no split; an unused slot, by its name | drop | unreachable; not placed |

Left out of the table, each with why:

- Pkmn Trainer Barry (607): a tag fight's partner beside the player (fights.json partners).
- Pkmn Trainer Lucas (613): a tag partner beside the player against two grunts.
- Pkmn Trainer Lucas (614): a tag partner beside the player against two grunts.
- Pkmn Trainer Lucas (615): a tag partner beside the player against two grunts.
- Pkmn Trainer Dawn (616): a tag partner beside the player against two grunts.
- Pkmn Trainer Dawn (617): a tag partner beside the player against two grunts.
- Pkmn Trainer Dawn (618): a tag partner beside the player against two grunts.
- Pkmn Trainer Barry (619): a tag fight's partner beside the player (fights.json partners).
- Pkmn Trainer Barry (620): a tag fight's partner beside the player (fights.json partners).
- Pkmn Trainer Lucas (621): a tag partner beside the player against two grunts.
- Pkmn Trainer Lucas (622): a tag partner beside the player against two grunts.
- Pkmn Trainer Lucas (623): a tag partner beside the player against two grunts.
- Pkmn Trainer Dawn (624): a tag partner beside the player against two grunts.
- Pkmn Trainer Dawn (625): a tag partner beside the player against two grunts.
- Pkmn Trainer Dawn (626): a tag partner beside the player against two grunts.
- Pkmn Trainer Barry (923): a tag fight's partner beside the player (fights.json partners).
- Pkmn Trainer Barry (924): a tag fight's partner beside the player (fights.json partners).
- Pkmn Trainer Barry (925): a tag fight's partner beside the player (fights.json partners).
- Ace Trainer Mickey (dummy_062): an unused dummy_ slot no map battles, which data.oxide_trainers() skips.
- Ace Trainer Angelica (dummy_063): an unused dummy_ slot no map battles, which data.oxide_trainers() skips.
- Ace Trainer Angelica (dummy_251): an unused dummy_ slot no map battles, which data.oxide_trainers() skips.
- Ace Trainer Mickey (dummy_387): an unused dummy_ slot no map battles, which data.oxide_trainers() skips.
- Ace Trainer Angelica (dummy_391): an unused dummy_ slot no map battles, which data.oxide_trainers() skips.

# The scorer's speed plan

Ian's goal (2026-10-02): a reading of the whole game by the fight scorer's
planner in a matter of hours, including the spread of boxes for each boss and
the very unlucky stress test, rather than the 500 hours he estimated from the
first timings. This doc keeps the plan and the evidence behind it.

The speed matters most at the end of the scorer's goals, which come in this
order (Ian, 2026-10-02):

1. A relatively quick Roark reading that passes its tests.
2. The three-gym split, through Fantina at cap 33, under the three-gym run's
   rules, with every major fight passing. Roark, Mars 1 and Gardenia are held
   to their hand-played bars; the fights with no hand-played bar (the rival
   fights, Jupiter 1, Fantina) pass when Ian has read the scorer's line and
   reasoning and accepts it.
3. Every major boss, rival, named Galactic fight and Ace Trainer, after the
   Kaizo study's broad comb of the trainers.
4. Everything, the full rescore: the reading this plan aims to bring down to
   hours. The Scoring
Agent owns the work and records its progress in its status home,
`docs/oxide/trainer-scoring-handoff.md`; the steps that wait on Ian are in the
tracker's Scheduled list.

## Where the time goes (2026-10-02)

The planner (`tools/oxide/balance/plplan.py` on `scoring-step3-bar`) decides
each turn by playing every option forward to the end of the fight in the
simulator, about 100 play-outs per decision. The Overseer profiled it on
Roark, one process on an idle machine, at its default settings: about 18
seconds of one core per fight, 21 decisions. The Scoring Agent measured about
133 seconds per fight at its own settings with the machine fully loaded, down
from 606. The gap is partly settings and partly the machine: the i9-14900K
has 8 performance cores with two threads each and 16 efficiency cores, so the
CPU seconds a process reports rise when all 32 threads are busy. Speed is best
measured as fights finished per hour on the whole machine.

Inside a fight, by the profile:

- About 90% of the time is play-outs.
- About 40% goes to working out the trainer AI's exact choice odds, which
  re-scores every move under every chance roll (about 900,000 move scorings
  for two fights).
- About 45% goes to the short "who wins this exchange" simulations the
  play-out policy runs.
- About 10 million calls go to small lookups (a species' regular abilities,
  type effectiveness, the AI's effectiveness figure) that return the same
  answer every time for the same inputs.
- Setting a fight up takes about 12 seconds, much of it two million file
  checks in the data loaders' freshness test.

## The levers

| Stage | Lever | Expected gain | Effort | Status |
|---|---|---|---|---|
| 1 | Store repeated lookups, the AI's odds per position, and the setup's file checks, instead of recomputing them | 2 to 3 times | a day or two | approved tentatively (Ian, 2026-10-02) |
| 1 | Run under PyPy, a faster engine for the same Python code, installed portably in the home folder | 3 to 5 times | hours to test | measured 2026-10-02: no real gain, not used (below) |
| 2 | A learned position value on the GPU in place of play-outs | 10 to 50 times per decision | one to two weeks | working (2026-10-02): about a fiftieth of the cost per fight, play close to the play-out planner except at Mars 1 (below) |
| 3 | The simulator and AI rewritten in a compiled language | 30 to 100 times on the hot loop | weeks | in reserve |
| any | Stop running a fight once its three numbers are known to a set margin | up to half the runs | small | not chosen: Ian set a fixed 100 runs a trainer, 75 real and 25 very unlucky (2026-10-02) |
| 2, paired | The opponent AI made cheaper with identical results (below) | up to about 1.5 times now, more once play-outs shrink | days | an idea from Ian's brainstorm, not yet work |

Stages 1 and 2 together should bring a full-game reading to a matter of
hours. Stage 1 alone was expected to bring the 500 hours to roughly 50 to
100; measured, it did not (below).

## What stage 1 measured (2026-10-02)

| Measure | Before stage 1 | After stage 1 |
|---|---|---|
| Throughput, whole machine | 357 fights an hour (30 workers) | 407 fights an hour (29 workers) |
| Memory per worker | about 2.5 GB after one fight, growing | at most 188 MB at peak |
| Same seeds, same fights | | 24 of 24 identical, move for move |

The stored lookups now keep only the AI's final odds per position, key them
by two hashes, cap them and empty them each fight; the prepared fight is
frozen before the workers fork, and pools are sized by memory as well as
cores (the Scoring Agent, 55ae648e22). That ended the memory problem that
crashed WSL, but added only about 14% speed: the play-outs themselves are the
cost, and storing lookups does not shorten them.

PyPy ran the scorer with identical results but no real gain. The Overseer's
check on the same night: a bare loop runs 33 times faster under PyPy, so the
install is sound; the simulator alone with a fixed player runs 1.3 to 1.6
times faster; with the play-out policy it runs slower than CPython (0.65 to
0.7 times); planner decisions 1.36 times. The trainer AI and the simulator
are long chains of game-rule branches (fightai alone is about 3,700 lines),
and PyPy's JIT speeds up code that repeats the same path. Here each turn takes
different branches, so in a 19-second run the JIT built about 3,000 side
paths and threw away 750 compiled ones. Its settings for long, branchy code
made it slower still. The Overseer's 3 to 5 times estimate was wrong for
this code.

At 407 fights an hour, a reading of 200 fights at real odds and 200 very
unlucky takes:

| Goal | Fights simulated | Time |
|---|---|---|
| 1. Roark (500 real, 200 unlucky) | 700 | under 2 hours |
| 2. The three-gym split, about ten major fights | about 4,000, before choosing sixes | about 10 hours |
| 4. Everything, 459 fights | about 184,000 | about 450 hours |

So stage 1's levers are spent, and hours for the whole game need stage 2,
which replaces most play-outs. Ian started stage 2 the same night, and cut
each trainer's reading to 100 simulated fights, 75 at real odds and 25 very
unlucky, which takes the whole game from about 450 hours to about 113 at
today's speed before stage 2.

## What stage 2 measured (2026-10-02)

The Scoring Agent's full account, with the commands that rebuild every network,
is in its doc's "Stage 2" section; the data and weights live outside git in
`~/oxide-trials/scorer-stage2/` and are rebuilt from the code.

- Networks trained on plain play-outs (v2) played fast but badly, as they
  learned the play-out policy's misreadings: Roark 45 of 75 clean against the
  play-out planner's 70.
- Self-play, retraining on the network planner's own fights labelled by how
  each ended, made it worse twice (Roark 40, then 3, of 75 clean): one
  fight's outcome is too noisy a label. It is set aside.
- Distillation worked: the network learns the play-out planner's own
  look-ahead values (1.2 million positions from 609 fights, 70 minutes on 29
  workers). The network d1b, on our sixes at real odds (clean, won, faints a
  fight, 75 fights): Roark 69/75, 75/75, 0.093 against the play-out planner's
  70/75, 75/75, 0.067; Gardenia 1/75, 63/75, 3.227 against 1/75, 66/75, 2.880;
  Mars 1 64/75, 75/75, 0.293 against 73/75, 75/75, 0.027, the gap, which the
  next round (training on the positions the network's own play reaches) aims at.
- Cost: about 2.3 to 3.4 seconds of one core a fight, against 113 to 210 for
  the play-out planner. The whole game's 459 fights at 100 simulated fights
  each would take about an hour and a half on 29 workers, before the spread
  of boxes for each boss: Ian's "matter of hours" is in reach once the
  network's play matches the play-out planner's.

## The opponent AI, cheaper with identical results (Ian's brainstorm, 2026-10-02)

The trainer AI is about a third of a decision's time on the stage 1 code (the
simulator's turns and the exchange simulations take most of the rest), so an
AI that cost nothing would speed decisions about 1.5 times. Once stage 2
replaces most play-outs, the AI's exact look-ahead becomes the larger share,
and these pay off more. Three ways, which stack:

1. Specialise it to each fight. The trainer's six, their moves and the
   player's six are fixed for a fight, so much of what the AI checks each turn
   has the same answer every turn: each move's effect routine, its type
   effectiveness into each player Pokemon, immunities, the ability guess,
   which routines can apply. Work those out once per fight; each turn checks
   only what changes (HP, stages, status, weather, the last move, the dice).
2. Compute its odds directly. The planner now reruns the whole AI scoring
   once for every combination of its random rolls. Most rolls only add or
   subtract points from one move's score, so score each move once, note each
   random bonus as "+N with chance p", and combine them into the chance each
   move ends highest with the game's tie-break, branching only where a roll
   changes which checks run.
3. Generate the AI from the decomp's script rather than a hand translation,
   one function per routine, which matches the game by construction and is
   the cheap route to a compiled AI later.

Identical is proven, not assumed: the old and new AI run side by side on
millions of positions and must give the same odds every time, beside the 365
existing AI checks.

Stage 1 must not change any answer. The dice are keyed by seed, so the same
seeds must give the same fights, move for move, before and after: a run of
fixed seeds is compared in full, and any difference is found and explained
before the faster version is used. Under PyPy, set iteration order and hash
seeds are the likeliest sources of a difference. Shortening play-outs is not
part of stage 1, since it changes the planner's judgement; if it is ever
wanted, its measured effect on the three numbers goes to Ian first.

## Stage 2, the learned value

The planner keeps its exact look-ahead of a turn or two (every chance weighed
at its real odds, the trainer's choice computed from its AI) and asks a
network how good each resulting position is, instead of playing every branch
to the end.

1. Generate millions of positions from the planner's own simulated fights
   across many trainers, boxes and splits, each labelled with how the fight
   ended from it: the faints and whether it was lost.
2. Train a network that reads a position (each Pokemon's species, HP, status,
   stat stages, moves and item, and the field: weather and its turns, screens,
   hazards) and predicts those outcomes. It runs on the PC's RTX 4070 Ti SUPER
   (16 GB, visible from WSL); PyTorch is installed (see Hardware).
3. Each decision then needs one batch on the GPU in place of about 100
   play-outs.
4. Retrain on the improved planner's own games, the loop that made AlphaZero
   strong.

It keeps Ian's rule that good play arises on its own (2026-10-01): the
network learns which positions are good from outcomes, never from named
plays. Its cost is legibility, so the planner still shows each turn's options
with their values, the network is spot-checked against full play-outs on the
showcase seeds, and the three-gym run stays the exam.

Measured on 2026-10-02 (the handoff doc's "Stage 2" has the readings): the
network planner costs 2.3 to 3.4 seconds of one core a fight, against 113 to
210 with play-outs, so the whole game's 459 fights at 100 simulated fights
each take about an hour and a half on 29 workers. Step 1's labels work best
taken from the play-out planner's own look-ahead (distillation): its best
network so far matches the play-out planner at Roark and Gardenia and trails
it at Mars 1. Step 4, self-play labelled by fight outcomes, made the network
worse in two rounds and is set aside. Later the same day, the average of
three distilled networks met the Roark and Mars 1 bars. A network trained
without a trainer's positions cannot play that trainer (Gardenia, 2 won of
500), so the whole game first needs labelled positions from every trainer.
At the rate of the rounds so far (about 400 positions a second on 29
workers), a few play-out fights for each of the 459 trainers is a one-off
job of several hours, after which a full reading takes about an hour and a
half; whether one network then judges trainers well enough is untested.

## Hardware (2026-10-02)

- CPU: Intel i9-14900K, 8 performance and 16 efficiency cores, 32 threads.
- Memory: 31 GB visible in WSL.
- GPU: NVIDIA RTX 4070 Ti SUPER, 16 GB, CUDA visible in WSL.
- Python 3.14 with numpy; no scikit-learn, and no PyPy yet (stage 1 installs
  it).
- PyTorch 2.14.1, built for CUDA 13.0, installed on 2026-10-02 at Ian's word
  in its own environment, `~/venvs/oxide-ml` (made with `uv`, seeing the
  system's packages too; 5.2 GB, removed by deleting the folder). Run it as
  `~/venvs/oxide-ml/bin/python`. Checked the same day: it sees the GPU, a
  matrix product matches the CPU's, the card reaches about 30 TFLOP/s in
  float32, and a small three-layer network of the kind stage 2 would train
  judges about 5.9 million positions a second, against roughly a hundred
  play-outs a second on one CPU core. Installing it does not start stage 2,
  which still waits on Ian's word.

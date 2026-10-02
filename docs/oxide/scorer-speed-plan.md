# The scorer's speed plan

Ian's goal (2026-10-02): a reading of the whole game by the fight scorer's
planner in a matter of hours, including the spread of boxes for each boss and
the very unlucky stress test, rather than the 500 hours he estimated from the
first timings. This doc keeps the plan and the evidence behind it. The Scoring
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
| 1 | Run under PyPy, a faster engine for the same Python code, installed portably in the home folder | 3 to 5 times | hours to test | approved tentatively (Ian, 2026-10-02) |
| 2 | A learned position value on the GPU in place of play-outs | 10 to 50 times per decision | one to two weeks | waits on Ian, after stage 1 and the Roark check |
| 3 | The simulator and AI rewritten in a compiled language | 30 to 100 times on the hot loop | weeks | in reserve |
| any | Stop running a fight once its three numbers are known to a set margin | up to half the runs | small | not yet put to Ian |

Stages 1 and 2 together should bring a full-game reading to a matter of
hours. Stage 1 alone should bring the 500 hours to roughly 50 to 100.

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
   (16 GB, visible from WSL); PyTorch is not yet installed (about 3 GB with
   pip).
3. Each decision then needs one batch on the GPU in place of about 100
   play-outs.
4. Retrain on the improved planner's own games, the loop that made AlphaZero
   strong.

It keeps Ian's rule that good play arises on its own (2026-10-01): the
network learns which positions are good from outcomes, never from named
plays. Its cost is legibility, so the planner still shows each turn's options
with their values, the network is spot-checked against full play-outs on the
showcase seeds, and the three-gym run stays the exam.

## Hardware (2026-10-02)

- CPU: Intel i9-14900K, 8 performance and 16 efficiency cores, 32 threads.
- Memory: 31 GB visible in WSL.
- GPU: NVIDIA RTX 4070 Ti SUPER, 16 GB, CUDA visible in WSL.
- Python 3.14 with numpy; no PyTorch, no scikit-learn, no PyPy yet.

# The counterpiece check

## Summary

The counterpiece check tells you, for certain, when a change to a boss team makes the fight too easy. It does not tell you the fight is right. It plays a candidate team against the six the scorer chose to beat the old team on each box, using the scorer's own planner (`plteam.full_reading`: 75 fights at real odds and 25 very unlucky ones). It runs on each box as the old reading built it and skips only the team search, so a run takes 25 to 30 minutes a box where a full reading takes hours.

The logic is one-sided. A full search could only find the player a stronger six than the old one. So if the old six still wins about as often as it beat the old team (within the scorer's tolerance), or wins more often than the fight's target, the candidate is too easy, for certain. A lower result proves nothing: a full reading might find a six that does better, so it only says the full reading should decide.

Since Ian's ruling of 2026-11-02 that the scorer is a ceiling and not a target, the check answers one question: does this change make the fight clearly harder? It does not tell you whether the fight reaches a band.

Its one limit is that it needs the old reading's own tree. The boxes re-rolled on `oxide` on 2026-11-02, when the Veilstone Elekid gift was removed, so a reading from before then cannot be rebuilt on today's tree. A candidate tree is made from that old tree with `plcounter tree`.

The code is `tools/oxide/balance/plcounter.py`, its test `tools/oxide/balance/test_plcounter.py`.

## What it does

Each box is rebuilt by `plgoal3.setup` under the old reading's run name, so its level, items, history (rules A and B) and seed are the reading's own. The driver refuses a box that differs from the one the reading recorded: members, level, starter or history. The six takes the reading's moves, and its items follow from them as they did. Only the trainer's team changes, and it changes because the tree the driver runs in holds the candidate's trainer file. No scorer function is patched.

The first trial of a box replays the reading's own dice, so a candidate that changes nothing reproduces the reading's numbers. The result per box is the share won, the average faints and the clean rate, at real odds and very unlucky, with the old reading's figures beside them.

A box's verdict is "too easy (old six wins as often)" when its won rate is within the tolerance of the old reading's, "too easy (over the target)" when it is over the target given with `--target`, and "reading decides" otherwise.

## Validation

Byron's team as it stood, played against the sixes of run `byron-0db1aeaee`, came out 100 percent won with 0.87 and 0.68 faints on boxes 1 and 2. The reading itself gave 100 percent with 0.85 and 0.73. The check reproduces the reading. The third box agrees too (99 percent and 0.58 against 100 and 0.51), and the check was run twice on that team, with the same result both times. The validation on Cyrus 1 (run `cyrus-1-61b9d0391`) was cancelled before it produced a result.

## Results so far

All rows are percent won, then average faints, at real odds, one trial on the reading's dice. "Old" is the old reading's own figure for the same box. Result files are in `~/oxide-trials/goal3/counterpiece/`.

| Run | Box | Won | Faints | Very unlucky: won, faints | Old: won, faints | Verdict |
|---|---|---:|---:|---|---|---|
| Byron, control (no change) | 1 | 100 | 0.81 | 96, 0.76 | 100, 0.85 | too easy |
| Byron, control | 2 | 100 | 0.73 | 100, 1.28 | 100, 0.73 | too easy |
| Byron, control | 3 | 99 | 0.85 | 96, 1.28 | 100, 0.51 | too easy |
| Byron, Ian's redraft | 1 | 79 | 3.24 | 88, 3.48 | 100, 0.85 | reading decides |
| Byron, Ian's redraft | 2 | 93 | 2.56 | 88, 2.48 | 100, 0.73 | too easy (over 88) |
| Byron, Ian's redraft | 3 | 88 | 2.55 | 60, 4.04 | 100, 0.51 | reading decides |
| Byron, Vikavolt version | 1 | 92 | 3.44 | 96, 3.44 | 100, 0.85 | too easy (over 88) |
| Byron, Vikavolt version | 2 | 96 | 2.20 | 100, 2.40 | 100, 0.73 | too easy (over 88) |
| Byron, Vikavolt version | 3 | 87 | 2.81 | 76, 3.40 | 100, 0.51 | reading decides |
| Barry 5, S1 Chople Berry on Empoleon | 2 | 100 | 0.55 | 100, 0.68 | 100, 0.05 | too easy |
| Barry 5, S2 Earthquake for Iron Defense | 2 | 100 | 0.19 | 100, 0.28 | 100, 0.05 | too easy |
| Barry 5, S3 Snorlax Immunity | 2 | 100 | 0.65 | 100, 0.72 | 100, 0.05 | too easy |
| Barry 5, S4 Greninja in Turtonator's slot | 2 | 100 | 0.59 | 96, 1.48 | 100, 0.05 | too easy |
| Barry 5, S1 and S4 together | 2 | 100 | 1.11 | 100, 1.48 | 100, 0.05 | too easy |
| Barry 5, T1 Charcoal on Infernape | 1 | 100 | 0.95 | 100, 1.80 | 99, 0.95 | too easy |
| Barry 5, T2 Snorlax Immunity | 1 | 97 | 1.49 | 88, 2.40 | 99, 0.95 | too easy |

Byron's target was 88 percent won and Barry 5's was 95. Ian's Byron redraft and the Vikavolt version were run for `docs/oxide/byron-ian.md`: the redraft pools to 87 percent won with 2.78 faints, a reading for the full scorer to settle, and Vikavolt reads easier than the redraft on boxes 1 and 2, which led Ian to take Galvantula back. Barry 5's dials are in `docs/oxide/barry5-dials.md`: no dial brought a version under the ceiling, since the reading's own six still wins 97 to 100 percent of its fights. In several Barry runs the player's faints rose a long way (0.05 to 1.11 on the Scorbunny box) with the win rate unchanged, which is a harder fight in a way the check's verdict does not show.

## How to run it

Make a tree for the candidate from the old reading's tree. A `--file` is a whole trainer file, a partial file (such as a `party` and `ai_flags`) laid over the base tree's, or another tree whose file to take.

```
python3 -m tools.oxide.balance.plcounter tree BASE_TREE DEST --file leader_byron=candidate.json
```

Then run the check from inside that tree, under the memory cap, with the old reading's run directory, the fight's slug and a name for the candidate.

```
cd DEST && PYTHONPATH=. tools/oxide/capped --max 10G python3 -m tools.oxide.balance.plcounter \
    read ~/oxide-trials/goal3/byron-0db1aeaee byron --name C3 --target 88
```

Options: `--boxes` picks box seeds (default all three, which can run as separate jobs), `--trials` adds full readings a box (the first replays the reading's dice), `--procs` sets the processes (default 8), `--target` is the fight's highest acceptable percent won, and `--out` names the result file (default `~/oxide-trials/goal3/counterpiece/<run>-<name>.json`). It prints a table and writes the JSON. A box takes 25 to 30 minutes at five processes; two runs at a time with 10 GB or more free has worked.

The test, `python3 tools/oxide/balance/test_plcounter.py`, passes 7 of 7: the verdict rules, the pooling, the rebuild of a six on the reading's dice, the table, and the refusal of a box that differs from the reading's.

## What the ruling changes

The ruling of 2026-11-02, from `.claude/rules/standing-rulings.md`: "Those targets are a perfect player's, so they no longer gate a fight (Ian, 2026-11-02): the scorer is a ceiling, since it knows the AI exactly and plays the best six from the whole box, and Ian plays his own lines, generally worse. Every fight built on judgement read 95 to 100 percent won, his hardest Byron included ('I genuinely don't think I could easily conceive a harder team'), so a boss need only be clearly harder than before, the playtest decides, a reading is asked for only when a fight looks trivial (under about one faint a fight), and the scorer's lines serve after a fight to show Ian what the line could have been."

So the check now shows whether a change makes a fight clearly harder, not whether it reaches a band. A "too easy" verdict on a change meant to harden a fight says the change did not make it clearly harder. A "reading decides" verdict says it might have, which is for Ian's judgement and, if he names the fight, a full reading.

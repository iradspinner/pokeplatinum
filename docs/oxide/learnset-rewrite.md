# The learnset rewrite (step 4)

Step 4 of `docs/oxide/learnset-checks.md`: the locked rules of
`learnset-insights.md` become checks and a generator, and the generator
rewrites every level-up list. The branch is `balance-learnset-rewrite`, cut
from `oxide` at da6b92496c (Poison Fang landed). Nothing lands until step 5
passes and Ian says yes.

## Summary (2026-10-06, stage 1 of 4 done)

**Outcome so far.** Sixteen new checks (7 to 22) read the locked rules and
the mechanical ones, each with a test against a case Ian judged in the
insight sessions; all 16 tests pass. Run on Oxide's lists before the
rewrite, they are the new baseline below. Oxide's lists fail every rule
somewhere. The largest gaps are coverage (215 of 222 final forms reach
fewer than three coverage types by level-up), steady learning (286 of 447
stages have a split with fewer than two new moves) and late moves (153 of
222 final forms learn nothing from 61 on). No list has been rewritten yet.

**Ian's action items.** None yet. The thresholds each check uses are the
defaults the rules state or imply ("How the checks read the rules", below);
they come to Ian with the rewrite's report, beside what the rewrite scores
on them, so he sets them once with both columns in front of him.

**Next steps.**

| Stage | What | Who | About how long |
|---|---|---|---|
| 2 | The generator, and all 652 level-up lists rewritten on the branch | Balance Agent | a long working session (most of a day) |
| 3 | The moves under review: Fury Attack and Feint out, rework questions written for Ian | Balance Agent | an hour, alongside stage 2 |
| 4 | The check 6 sheets regenerated for the rewrite; the gate run; this report finished | Balance Agent | an hour |
| Step 5 | The exam judged by a reviewer who did not write the lists; the bosses read against their bands | Overseer, Scoring Agent | the Scoring Agent's boss reading takes hours of machine time |

## Ian's ruling during step 4

Ian, 2026-10-06, to the Balance Agent: additions to a level-up list come
from the whole pool of moves Oxide has; later games' learnsets (hg-engine's,
or looked up) are inspiration, not pick lists. The generator therefore
considers every working move for every line, scored by fit (type, stats,
abilities, role), and a move a later game, Generation 4 or Kaizo gives the
line counts in its favour without limiting the choice. It supersedes, for
level-up lists, the rule of 2026-09-27 that only later games' level-up moves
come in and TM, tutor and egg moves wait for the TM pass.

## The new baseline: Oxide's lists before the rewrite

Checks 1, 4 and 5 are the step 1 checks, rerun. Check 1 now leaves out the
moves no list may rely on (below), so it finds 59 failing stages where the
step 1 baseline found 51. Checks 2 and 3 are the scoring track's matchup
screen on Oxide's lists (`~/oxide-trials/learnset-baseline/checks-2-3.md`):
of 86 lines that met a boss in their window, 38 were taken by none (leads,
not verdicts) and 20 by every boss that met them.

| Check | Rule | Oxide |
|---|---|---|
| 1 | An own-type attack of 50 within a split (447 stages) | 59 fail, 21 of them with none by 78 |
| 2 | A niche: in a boss's top six in the line's window (86 lines met a boss) | 38 taken by no boss |
| 3 | No dead and no universal moves | the scoring track's tables |
| 4 | No fixed or level damage by Gardenia's end; no one-hit KO move | 5 entries; 28 one-hit KO moves |
| 5 | Ian's move rules (PP, weather, accuracy, TM list) | 14 stat-lowering moves off their PP rule; 14 removed TMs still listed |
| 7 | R1, five or six moves by the first split's cap, at most one filler (199 lines) | 67 fail |
| 8 | R2, two new moves in each split a stage is held at the cap (447 stages) | 286 fail |
| 9 | R4, the first coverage move by the second split (199 lines) | 105 fail |
| 10 | R5, three coverage types over the game, two for a very strong line (222 final forms) | 215 fail |
| 11 | R6, no move dominated by a stronger one already had | 4 entries |
| 12 | R7, a good utility move by the second split, two over the game for a less offensive line (222) | 97 fail |
| 13 | R8, no evolution or learn-level choice inside one split | 68 free holds, 212 same-move pairs |
| 14 | R11, an attack of each of the stage's types within a split (447 stages) | 81 fail |
| 15 | R21, Baton Pass only with a boost to pass | 2 species |
| 16 | R24 and the removed moves off every level-up list | 218 entries |
| 17 | R25, no move below the level a stage is first had at | 133 entries |
| 18 | R32, a setup move only beside an attack it boosts | 24 entries |
| 19 | R37, no attack under 90% accuracy | 165 entries |
| 20 | Every evolution needing a known move reachable by level-up (10) | 1 fails: Sylveon |
| 21 | A real level-up move from 61 on each final form (222) | 153 fail |
| 22 | One move a level, none past 78, no move twice | 62 shared levels, 36 past 78, 1 twice |

Check 5's PP findings are move data, outside the learnset rewrite; they
stay with the tracker's open PP item. Check 16 also finds 651 entries on the
TM and tutor lists (Protect and Double Team on nearly every TM list), which
the TM pass clears.

Some of the cases the checks find, each one Ian named:

- Check 7: Charmander has Scratch, Growl, Ember and Smokescreen by Roark's
  cap once Dragon Rage is gone, three of them filler; Abra has Teleport,
  which leaves the game, and nothing else.
- Check 8: Charmeleon learns only Scary Face in Gardenia's split; Alolan
  Ninetales learns nothing in ten splits.
- Checks 9 and 10: the Charmander line reaches no coverage type by level-up,
  where Kaizo gives it Dark, Flying and Steel.
- Check 14: Steelix has no Ground attack, Glalie no Rock attack, Charizard
  no Dragon attack, Togetic no Fairy or Flying attack.
- Check 15: Togetic's Baton Pass, with no boost on the line.
- Check 17: Glalie's Ice Beam at 37, below its evolution at 42; Roselia's
  whole early list below 30.
- Check 18: Altaria's Dragon Dance with Take Down its only strong physical
  attack; Budew's Growth with Mega Drain.
- Check 20: no player Eevee can learn Charm, so Sylveon is unreachable.

`PYTHONPATH=. python3 -m tools.oxide.balance.learncheck rules` prints every
failure by name; `summary` prints checks 1, 4 and 5.

## How the checks read the rules

Every check reads the lists as the player meets them, by the capture rule
and on-time evolution (the step 1 baseline's "How the checks read the
data"). A line is walked from its earliest catch, down every branch. The
numbers in brackets are the defaults, each Ian's to change.

- **Moves no list may rely on.** The rampage moves (R9, until they are
  one-turn), the moves waiting on Ian's rework (Fury Cutter, Psywave, the
  two-turn attacks that are neither setup nor Solar Beam and Solar Blade,
  every multi-hit move), the moves leaving the game (Fury Attack, Feint, the
  first cut of 2026-09-27, Splash, Teleport, Steel Roller, Ice Spinner),
  R24's moves, fixed and level damage, and status moves whose effect the
  engine does not carry out. None counts toward any check, check 1
  included.
- **Check 7, R1.** The moves by the first split's cap that count (all but
  the above and the moves Ian rated useless or terrible), on the best catch
  and branch in that split. Filler is a move Ian rated bad (Growl, Leer,
  Tackle, Bind and the rest) or a plain Normal attack of 40 or less on a
  Pokemon that is not Normal (Scratch, Pound). Pass: five moves, at most one
  filler (5 and 1).
- **Check 8, R2.** The new moves a stage learns in each split it is held at
  the cap: from the split after it is had, until the split it evolves in by
  level; while its own list teaches, if it evolves by an item; to the
  League, if it is final; and from three splits after its item, if an item
  made it final (R10). Pass: two in every such split (2).
- **Check 9, R4.** The first coverage attack (not of the holder's types,
  not Normal, 40 or more by effective power, on a stat at least 80% of the
  holder's better attacking stat, R15). Pass: by the end of the second split.
- **Check 10, R5.** Distinct coverage types the final form has by 78
  (attacks of 50 or more, fitting the final form), with Kaizo's types for the
  line beside them. Pass: three, or two for a final form of 580 total stats
  or more (R35).
- **Check 11, R6.** An entry learnt while a stronger, at least as accurate
  move of the same type and class is had, where the entry has no secondary
  effect and no priority (the narrowing of 2026-10-06).
- **Check 12, R7.** Ian's tiers, by move and by class (every Speed and
  attack raiser is SSS, every blocking move fantastic, every attack that
  always lowers Speed incredible); a status move he has not rated takes the
  Generation 9 list's tier a step down. Pass: a good move (Good or better)
  by the end of the second split, and two over the game when the final
  form's better attacking stat is under 85.
- **Check 13, R8.** A free hold is a move the pre-evolution learns between
  its evolution level and that split's cap, which the evolved form lacks by
  the cap. A same-move pair is one move on both lists at two levels inside
  one split.
- **Check 14, R11.** Each of a stage's types has an attack of any power
  within a split of the stage being had, exempt where check 1 exempts.
- **Checks 15 to 22.** Baton Pass needs a stat-raising move on the line;
  R24's moves and the removed moves on any level-up entry; an entry below
  the lowest level the stage can be had at, learnt by no earlier stage and
  not again later; a setup move needs a strong same-type attack it boosts,
  or two strong attacks it boosts, by the end of the next split (80 by
  effective power, same-type at one and a half); attacks under 90%; known-move
  evolutions; a move from 61 on each final form; and list hygiene.

## Two corrections to the catch data

Ian named two errors in the balance tools' catches during the insight
sessions. The checks apply both; the pool the stored scores read is left
alone, so no score goes stale.

- Amity Square's table has no map header, so no one can meet it: its 16
  catch rows are left out (Swablu is now first caught on Route 210 in
  Maylene's split). The encounter track owns wiring or explaining it.
- Cynthia's Togepi egg is received in Fantina's split, after the Eterna
  building, not in Gardenia's.

# Fixing the play-off: the plan for Ian's sign-off

All four defects the QA pass of 2026-10-21 found in the play-off (its findings 3 to 6) are real on the boxes. Three fixes are small and add no fights. The fourth, swaps kept on luck, needs more than the race's five-point tolerance, which on its own barely helps, so the plan adds a short confirmation read. Ian decides two things: whether to approve the four fixes, and for the luck defect, the tolerance alone or the tolerance with the confirmation read (recommended). The work takes about two hours with its tests, and the readings would cost at most about 6 percent more fights a box from Barry 3 on.

Every number below comes from the 36 boxes of the boss fights from Roark to Wake, seeds 1 to 3, built as the QA pass built them, with the real screen. No real play-off has run yet (the rehearsal's finalists held no held version), so defects 2 and 3 were measured with fights decided by a hash, where no swap is truly better than another.

## 1. A hold tested without its own move

The play-off plays a held version with the moves its hold brings. Where the hold brings three or more, it plays the first two alphabetically, and it can overwrite a pick that is itself one of the hold's moves. On the 36 boxes, 18 of 474 held versions play without the move the hold exists for, all from Barry 3 on (the QA pass's 12 of 271 reproduce on its 27 boxes, which leave out the rivals, and Lucas and Dawn 2, Barry 3 and Barry 4 add the rest). Liepard (Purrloin held to 36) exists for Sucker Punch and plays Captivate and Nasty Plot instead. Held to 37 and to 39, it plays the same four, so three holds are one test repeated. Masquerain (Surskit held to 43) loses Baton Pass, the screen's own pick, to Agility and Mist. The fix: the box records which move each hold is for (the one learned at the hold's level), and the play-off puts that move in first, then the hold's other moves, never over the first two picks or over a pick the hold brought. The same check then finds 0 of 474 without their move, and Liepard held to 36 plays Dark Pulse, Bullet Seed, Captivate and Sucker Punch. The tests that fail today: Sharpedo (Carvanha held to 38), whose picks already carry Take Down, and Liepard held to 36, with three moves gained, must each play its hold's move.

## 2. Swaps kept on luck

Each swap is read on its finalist's own race fights, 28 to 32 of them, and kept if it scores higher by any amount. Every finalist from Barry 3 on has swaps (3 at the median, up to 11), and the best of several noisy readings usually beats the finalist: with hash fights, 37 of 108 finalists changed. Requiring the race's tolerance, five points, cuts that only to 30, since one fight is worth three or four points. The recommended fix: a swap must lead by more than the tolerance, and is then read beside its finalist on 25 fresh fights and kept only if it still leads by more than the tolerance there. In a model of the same fights, this keeps a lucky swap for about a quarter of the finalists that have swaps (half today). It keeps a swap that truly wins 20 points more about 9 times in 10, and one 10 points better about 4 times in 10, as today. Afterwards, fewer boxes set off the paired reading, and fewer seeds commit their later fights to a hold under rule B, for nothing. The tests that fail today: a stubbed swap leading by three points, and one leading by eight on the race's fights but trailing on the fresh ones, are both kept now and must not be.

## 3. Rewritten moves left behind

The play-off rewrites the moves of every held version it tries and never puts them back. A version it did not keep then carries the new four into the improve loop and any later reading, while the loop chooses by the screen's sums for the old four. On the 36 boxes, 97 versions were left rewritten, from one at Roark to seven on Wake's box 3. A second fault rides with it: a version tried for two finalists is rewritten twice, the second time from the first rewrite, and Breloom (Shroomish held to 37) on Wake's box 3 lost Giga Drain, its hold's move. The stubbed loop read no rewritten version on any of the 36 boxes (the QA pass saw one, a Donphan on Maylene's box 2), so a wrong six reaching the loop is rare. The fix: build a version's play-off moves from the screen's picks, and after each finalist restore the moves of every version not kept. The test: after a stubbed play-off, every version outside a kept six has the screen's four, and a version tried for two finalists plays the same four both times.

## 4. An equal held version always taken

The screen drops a version that is no better than another of its catch against any enemy. Where a held version is a little better against one enemy, the on-time version is the one dropped, so every six takes the held one, even where another member already answers that enemy and the six scores the same either way. In 17 of the 36 boxes, the screen's top sixes take such a version 110 times. On Wake's box 2, Cinderace (Raboot held to 44) is in 12 of the top 20 sixes, each at the on-time Cinderace's score, and on Moira 1's box 2, Raboot (Scorbunny held to 26) is in 14 of 20. The fix: never drop the on-time version, so a tie goes to it. Tried on those two boxes, the screen's scores are unchanged, the equal Cinderace and Raboot leave every top six, and Staraptor (Staravia held to 43), which raises its sixes' scores, stays in all 20. The test that fails today: Wake's box 2's screen takes the on-time Cinderace in those 12 sixes at the same scores.

## What the fixes cost

The play-off already plays about 500 fights a box from Barry 3 on.

| Fix | Fights added to a reading |
|---|---|
| 1, the hold's own move | none |
| 2, tolerance and confirmation | about 85 a box from Barry 3 on, about 6 percent of such a box's fights; at most about 3 hours on step 15's estimate of 35 to 45 |
| 3, moves restored | none |
| 4, ties to the on-time version | none, and it saves paired readings |

Fixes 2 and 4 also avoid paired readings, each a second search of its box, but how many cannot be counted without real fights.

## What was not verified

The hash fights treat every fight as independent, while the real play-off plays a swap on its finalist's own seeds, which may make real comparisons less noisy than the model; by how much is unmeasured. The boxes carry no earlier fights' choices (the QA pass's finding 1), as the QA pass's boxes did not.

# The learnset rewrite (step 4)

Step 4 of `docs/oxide/learnset-checks.md`: the locked rules of
`learnset-insights.md` become checks and a generator, and the generator
rewrites every level-up list. The branch is `balance-learnset-rewrite`, cut
from `oxide` at da6b92496c (Poison Fang landed). Nothing lands until step 5
passes and Ian says yes.

## Summary (2026-10-06, step 4's lists and checks done)

**Outcome.** The generator rewrote the level-up lists of 634 of the 653
species, from Oxide's lists as they were, so each list keeps what already
worked and every one of the 4,340 changes names its rule. Seventeen checks
read the locked rules (checks 7 to 23), each with a test from a case Ian
judged, and all tests pass. On the rewrite every check passes except a
handful of named cases, set out under "Ian's questions": no stage goes two
splits without a same-type attack (Oxide had 61), every line has five or
more moves in its first split but Unown and Wooloo, coverage reaches three
types on all but three final forms (Oxide: 7 of 226 did), and nothing is
lost below an evolution, dominated or left past 78. The one rule that runs
short is R2's two new moves per split, which holds through Byron's split
and falls away from HQ on, where lines run out of moves that fit them.
Lists average 16.8 entries, up from 14.0; the ROM builds.

**Checks 2 and 3** (the scoring track's screen) barely move the lines the
bosses take (36 taken by none against 38) and show the screen picking real
moves where it picked filler, but leaning on a few staple coverage moves.

**The stored scores** (B3 and B6) are recomputed on the new lists, all
1,030 verified by a second pass with no disagreement. No story fight moves
on Ian's fight scale and no ordinary trainer changes band (one pair, Hikers
Damon and Maurice, reads 3.4 where it read 4.2). That scale is built from
safe switch-ins, which turn on the player's types and bulk more than their
moves, so it barely sees a learnset change; the boss readings of step 15
are the real check of the rewrite's power.
Step 5 is these checks and the sealed exam, read by an independent
reviewer the Overseer runs on the lists at 47503db009; the rewrite lands
on those. No boss is read until the rewrite and the TM pass have both
landed (Ian, 2026-10-06): one goal 3 reading on the QA ROM then checks the
bosses against their bands (`alpha-readiness.md`, step 15). Nothing is
checked in game.

**Ian's action items**, each set out with its context below:

1. Rule on seven move reworks (recharge moves, charge-turn moves, the
   multi-hit moves, Fury Cutter, Psywave, Spite's PP, and one-turn Uproar
   and Raging Fury). A cloud job writes the engine side once he has.
2. Set the checks' thresholds, above all R2 late in the game.
3. Decide a few named cases: Unown and Wooloo, three thin coverage counts,
   16 inaccurate attacks with no accurate stand-in, three early
   fixed-damage moves, and the delay demons.
4. Say whether the generator should spread its coverage away from a few
   staple moves (Rock Tomb, Bulldoze, Iron Head) before the rewrite lands.

**Next steps.**

| Step | What | Who | About how long |
|---|---|---|---|
| 4 | Rescore, checks 2 and 3, the gate, then this report closed | Balance Agent | an hour or two of machine time |
| 5 | The checks above and the sealed exam, judged by an independent reviewer | Overseer | about an hour |
| Reworks | The engine side of Ian's rulings on the questions below | a cloud job | a session |
| TM pass | Rerun on the new lists, with the reward table and gauntlets | Balance Agent | 2 to 3 hours, then 2 to 3 to write it in |
| 15 | The bosses read against their bands, once on the QA ROM | Scoring Agent | hours of machine time |

## Ian's questions

### 1. The move reworks

These moves sit on player lists today, and no check counts them until Ian
rules, so no list relies on one. Each row gives Oxide's numbers, how many
lines the player can own learn it by level-up in the rewrite, Kaizo's
change where it made one, and a recommendation.

| Moves | Oxide now | Lines | Kaizo | Recommendation |
|---|---|---|---|---|
| Hyper Beam, Giga Impact | 150, 90%, recharge | 12 and 4 | 180, 100%, no recharge, half the damage as recoil | Kaizo's |
| Blast Burn, Frenzy Plant, Hydro Cannon | 150, 90%, recharge | 1 (Greninja's Hydro Cannon) | no recharge; a third as recoil and 20 to 30% status, or half as recoil | Kaizo's |
| Rock Wrecker, Roar of Time | 150, 90%, recharge | 2 and 1 | Rock Wrecker made a three-hit move | Hyper Beam's pattern |
| Sky Attack | 140, charge turn | 2 | 120, one turn, a third as recoil, 20% paralysis | Kaizo's |
| Dig, Dive | 80, a turn underground or underwater | 6 and 10 | one turn, Dig 60, Dive 80 | Kaizo's |
| Fly, Bounce, Phantom Force, Shadow Force | two turns, the user out of reach | 1, 17, 1, 1 | Bounce kept two-turn, 100% | keep them two-turn: the turn out of reach dodges an attack, so it is not a wasted turn as a recharge is |
| The two-to-five-hit moves | Fury Swipes 18, Double Slap and Arm Thrust 15, Spike Cannon 20, the rest 25; all 100% | 19, 11, 5, 5; Bullet Seed 8, Pin Missile 9, Rock Blast 14 | Fury Swipes and Double Slap to 30, Pin Missile, Bullet Seed and Icicle Spear to 25; Comet Punch, Spike Cannon, Arm Thrust and Barrage replaced | bring every two-to-five-hit move to 25 a hit (about 77 in all, Generation 5's spread of hits) and keep them all; cut none further, since each type's one is a line's Technician or Skill Link tool |
| Fury Cutter | 40, doubles each turn | 10 | 30, three hits rising by 10, as Triple Axel | Kaizo's |
| Psywave | random damage of 50 to 150% of the user's level | 3 (Chimecho, Lunatone, Solrock); Misdreavus knows it at capture | replaced | cut it, and give its three lines Psybeam at the same level |
| Spite | 10 PP | 8 | not changed | Ian ruled limited PP for PP stalls: 5, inside the 3 to 6 of the stat-lowering moves |
| Uproar | 90, two to five turns locked | 9 | no version (Kaizo lacks it) | one turn, 100 power, 20% to confuse (Petal Dance's pattern), so it does not copy Hyper Voice's 90 |
| Raging Fury | 120, locked | 0 | no version | one turn, 120 power, a third as recoil, 20% to confuse (Thrash's and Petal Dance's pattern) |

The rampage moves are ruled already: Thrash, Petal Dance and Outrage
become Kaizo's one-turn versions. A list places them at that worth, so a
placement that would be an early spike once the engine lands moves later
(Larvitar's Thrash from 23 to 61). The placements waiting on the engine
change: Thrash on 10 lines (Croconaw, Larvitar, Mankey, Pupitar and
Totodile at 61; Annihilape, Feraligatr, Nidoking, Primeape and Tyranitar
at 66), Petal Dance on 3 (Cherrim and Roselia at 45, Arboliva at 58), and
Outrage on 10 (Hakamo-o and Jangmo-o at 61; Gabite, Goodra, Hisuian Goodra,
Litten and Torracat at 66; Annihilape and Incineroar at 69; Kommo-o at
70), Gabite's being a delay demon's prize.

### 2. The thresholds

Each check's numbers are the defaults the locked rules state or imply. The
one that decides the most is R2's.

R2 asks two new moves of every stage in every split it is held at the
cap. The rewrite meets it through Byron's split (14 short splits of 580),
then falls away: short on 20 of 203 held splits in Candice's, 66 of 213 in
HQ's, 90 of 219 in the Galactic split, 149 of 222 in Volkner's, 196 of 226
in Barry's and 207 of 226 in the League's. Volkner's and
Barry's splits are three levels each, and by then most lines have every
move that fits them. Filling the count anyway gave Garchomp Wish and
Synthesis and every final form Swagger, which a player would read as
junk, so the generator leaves a split short instead.

Recommendation: from HQ's split on, R2 asks two new moves over each pair
of splits (HQ with the Galactic split, Volkner's with Barry's) and one in
the League's. Every final form keeps a real move from 61 on, which the
rewrite meets on all 226.

The others, kept unless Ian changes them:

| Check | Default |
|---|---|
| 7, R1 | five moves by the first split's cap, at most one filler |
| 9, R4 | first coverage attack of 40 or more by the end of the second split |
| 10, R5 | three coverage types by 78; two for a final form of 580 total stats or more |
| 12, R7 | a good utility move (Ian's Good or better) by the second split; two over the game when the final form's better attacking stat is under 85 |
| 18, R32 | a setup move needs, by the next split, a same-type attack it boosts of 80 or more by effective power with the same-type bonus, or two attacks it boosts |
| 19, R37 | under 90% accuracy is flagged |
| 23, R16 | at least one move from after Generation 4 on every line |

### 3. Named cases

- **Unown** knows only Hidden Power, so it fails R1, R4, R5 and R7 by
  design. Recommendation: exempt it.
- **Wooloo** has three moves by Roark's cap: Tackle, Round and Guard
  Split. Nothing else that fits passes the ceilings and the no-filler
  rule; Double Kick, its natural second move, waits on the multi-hit
  ruling. Recommendation: accept it until then.
- **Coverage:** Magnezone and Pheromosa reach two coverage types (Kaizo
  gives them one and none). Articuno and Lunatone learn no move from after
  Generation 4: nothing newer fits them by level-up. Recommendation: accept
  all four.
- **Accuracy:** 16 attacks under 90% stay because no accurate move of the
  type comes within 85% of their average damage: Megahorn on eight lines
  (Clodsire, Goldeen and Seaking, Heracross, Nidoking, Rhyhorn, Rhydon and
  Rhyperior), Power Whip on four (Goodra, Hisuian Goodra, Lickitung,
  Lickilicky), Head Smash on three (Cranidos, Rampardos, Relicanth), and
  Greninja's Gunk Shot. R37 calls them very hard to justify.
  Recommendation: keep Head Smash, the fossils' signature, and swap the
  rest for the line's best accurate move of the type (X-Scissor for
  Megahorn, Leaf Blade or Seed Bomb for Power Whip, Poison Jab for Gunk
  Shot), giving up some power for no gamble.
- **Early fixed damage** (check 4): by Gardenia's end, Buizel knows Sonic
  Boom at capture at 3, Machop learns Seismic Toss at 19 and Murkrow Night
  Shade at 21. In Fantina's split Duskull, Gastly and Litwick know Night
  Shade at capture at 15 and Yamask at 16, Misdreavus knows Psywave at 15
  and Gible Dragon Rage at 18. Charmander's and Charmeleon's Dragon Rage
  are gone, as ruled. Recommendation: move each out of the split it
  starts in, as Ian ruled for Charmander.
- **Delay demons** (R19): four lines earned a payoff for holding a middle
  stage past 66: Gabite learns Outrage, Pupitar and Croconaw Dragon Dance,
  Grotle Shell Smash. The generator gives a payoff only where it is big
  (an attack of 100 or more stronger than the final form's, or an SSS
  setup move the line is linked to), so Luxio's kind (the middle stage
  learning the big moves sooner) is not built. Recommendation: keep these
  four, and say if Luxio's kind should be built too.
- **Steelix** comes from a Metal Coat in Gardenia's split, which Ian ruled
  too early (R13). That is the item's placement, for the item pass, not the
  lists.

### 4. Staple coverage (check 3)

The screen behind check 3 (below) shows the rewrite's coverage leaning on a
few staple moves: among the screened team members, Rock Tomb is known by
922, Bulldoze by 896, Iron Head by 618, Earthquake by 588, Bite by 553 and
Ice Beam by 545. Earthquake was already the screen's top pick on Oxide's
lists, but Rock Tomb, Body Press and Iron Head are new near-universal
picks, which check 3 ("no universal moves") sets against. The generator
can weigh a move down by how many lines already have it, which spreads
coverage over the types' other moves (Smack Down, Rock Slide and Stone
Edge's accurate kin; Mud Shot and High Horsepower; Flash Cannon and Steel
Wing). Recommendation: yes, before the rewrite lands. It changes lists, so
the scores and checks run again (about an hour of machine time), and the
exam is read on the new lists.

### 5. Two notes for the TM pass

R5's coverage by level-up draws most on staple TM moves: Bulldoze is new
on 66 lines' lists, Rock Tomb on 64, Ice Beam on 52, Icy Wind on 50 and
Earthquake on 43. The TM pass, which makes TMs single-use, should count
those as already covered. And Ian's ruling of 2026-10-06 (below) now lets a
level-up list take any working move, so the TM pass need not hold a move
back for being TM-only in later games.

## Ian's ruling during step 4

Ian, 2026-10-06, to the Balance Agent: additions to a level-up list come
from the whole pool of moves Oxide has; later games' learnsets (hg-engine's,
or looked up) are inspiration, not pick lists. It supersedes, for level-up
lists, the rule of 2026-09-27 that only later games' level-up moves come in
and TM, tutor and egg moves wait for the TM pass.

The generator applies it with two narrowings, which Ian accepted for alpha
1 the same day (relayed by the Overseer):

1. A status move it adds must already be linked to the line (Oxide's own
   lists, canon by any way, or Kaizo's lists); an unlinked attack comes in
   only to fill a gap a rule asks for (R11, check 1, R4, R5's count, R7,
   R30, R16 or the late move), never to make up R2's count.
2. The added attacks and utility moves keep under a ceiling for their
   split (the power and tier ceilings under "How the generator works").
   For this pass this sets aside his answer 8 of 2026-09-27, which put no
   ceiling on coverage power.

The standing rulings and the Kaizo comparison record both on `oxide`.

## The checks: Oxide's lists against the rewrite

Checks 1, 4 and 5 are step 1's, run again; check 1 no longer counts the
moves no list may rely on. Checks 2 and 3 are the scoring track's screen
(`plniche.py`, run unchanged on 39 boss fights and 3 rolled boxes each;
its output is in `~/oxide-trials/learnset-rewrite/`, where its "oxide"
column is the rewrite and its "v3" column Oxide's lists before it).

| Check | Oxide | Rewrite |
|---|---|---|
| 2. Lines met by a boss in their window that no boss takes, of 86 (leads, not verdicts) | 38 | 36 |
| 2. Lines every boss that met them takes | 20 | 18 |
| 3. Moves known by a screened member, never picked | 134 of 433 | 173 of 442 |
| 3. The screen's most-picked moves | Earthquake, Tackle, Take Down, Crunch, Brave Bird | Earthquake, Taunt, Rock Tomb, Body Press, Iron Head |

The screen takes about the same lines with either version, since it ranks
by stats and type matchups first. It now picks real moves where it picked
filler (Tackle, Growl, Fury Attack and Double Team were among Oxide's top
twenty picks), and more moves go unpicked because the lists are longer
and the screen takes one attack of each type. The staple coverage is
question 4 above.

| Check | Rule | Oxide | Rewrite |
|---|---|---|---|
| 1 | An own-type attack of 50 within a split (454 stages) | 61 fail, 21 with none by 78 | 0 fail |
| 4 | Fixed or level damage by Gardenia's end; one-hit KO moves | 5; 28 | 3; 0 |
| 5 | Ian's move rules (move data, the same in both) | 14 stat-lowering moves off their PP rule | the same |
| 7 | R1, five moves by the first split's cap, at most one filler (203 lines) | 68 fail | 2 fail |
| 8 | R2, two new moves per split a stage is held at the cap (454 stages) | 293 fail | 215 fail, nearly all from HQ on |
| 9 | R4, the first coverage move by the second split (203 lines) | 106 fail | 1 fail (Unown) |
| 10 | R5, three coverage types over the game (226 final forms) | 219 fail | 3 fail |
| 11 | R6, no move dominated by a stronger one already had | 4 entries | 0 |
| 12 | R7, a good utility move by the second split (226) | 98 fail | 1 fail (Unown) |
| 13 | R8, no evolution or learn-level choice inside one split | 278 pairs | 0 |
| 14 | R11, an attack of each of the stage's types within a split (454) | 86 fail | 0 |
| 15 | R21, Baton Pass only with a boost to pass | 2 species | 0 |
| 16 | R24 and the removed moves off every level-up list | 218 entries | 0 |
| 17 | R25, no move below the level a stage is first had at | 133 entries | 0 |
| 18 | R32, a setup move only beside an attack it boosts | 24 entries | 0 |
| 19 | R37, no attack under 90% accuracy | 165 entries | 16 |
| 20 | Every evolution needing a known move reachable by level-up (10) | 1 fails: Sylveon | 0 |
| 21 | A real level-up move from 61 on each final form (226) | 155 fail | 0 |
| 22 | One move a level, none past 78, no move twice | 99 entries | 0 |
| 23 | R16, a move from after Generation 4 on every line (203) | 145 fail | 2 fail |

Every catch knows an attack at capture in the rewrite; nine species had a
catch that knew only status moves on Oxide's lists. Sylveon is reachable:
Eevee now learns Charm by level-up, by the general rule that a move an
evolution needs is learnable, with no look at Eevee in particular.

`PYTHONPATH=. python3 -m tools.oxide.balance.learncheck rules` prints every
failure by name, `summary` checks 1, 4 and 5, and `sheets` writes the
split sheets in `docs/oxide/learnset-sheets/`, which now set the rewrite
beside Oxide's lists for reading by split.

## How the generator works

`tools/oxide/balance/learngen.py` (`plan`, `write`, `show SPECIES`) starts
from each list as it was and changes only what a rule asks for, in four
passes. Its log, `tools/oxide/balance/learngen_log.tsv`, has every change
with its rule.

1. **Clean.** The moves leaving player lists or the game go (R24, Fury
   Attack, Feint, the first cut, the dead weight, Ian's useless and
   terrible moves, the moves that call a random move); a move good only
   for building a trainer's fight goes to level 1, the trainers' palette
   (R26); a phazing move stays only where a wild catch knows it (R18); an
   attack under 90% gives way to an accurate one of its type (R37); a
   rampage move sits where its one-turn worth fits (R9); nothing stays past
   78.
2. **Structure.** A move below the level a stage is first had at moves
   onto the pre-evolution's list where that species can learn it, else up
   to the stage's level (R25); a move the pre-evolution learns inside its
   evolution's split joins the evolved form at that level, and a copy that
   comes only by holding goes (R8); an evolution that needs a known move
   gets the move by level-up.
3. **Fill.** Each line is walked from its earliest catch, split by split.
   The first split is filled to five moves with little filler (R1); each
   later split a stage is held at the cap to two new moves (R2); and each
   addition is the best candidate for what the line lacks by then: an
   attack of each type (R11), a same-type attack of 50 (check 1), coverage
   by the second split and three types over the game (R4, R5), a good
   utility move (R7), a strong same-type attack on the final form (R30), a
   newer move (R16), a late move. Candidates are every working move Oxide
   has, scored by fit: its type and the stat it uses (R3, R15), the line's
   abilities (R31) and stats (R17), and a link to the line in its own
   lists, canon or Kaizo, which counts in its favour. A move that answers
   nothing due needs such a link; a status move always does. An added
   attack keeps under a power ceiling for its split (60 in Roark's, 75 in
   Gardenia's, 80 in Fantina's, 90 to Wake's, 100 to Candice's, more
   after; a strong line a split later, coverage lower), adds something
   over the line's moves of its type (R6), and is never under 90% (R37);
   a utility move keeps under a tier ceiling (good in Roark's split,
   incredible in Gardenia's, fantastic in Fantina's). Then R19's delay
   demons and a settle pass (R21, R32, R6, R8, R25 again).
4. **Tidy.** One move a level, no move twice, at most 34 entries (the
   engine's limit), every catch knowing an attack, no wild catch knowing a
   move that ends the encounter.

A line the player cannot own (the post-game legendaries, the lines no
table reaches) gets the clean and the tidy only. `test_learngen.py`
checks that the writer round-trips every species file, that the files are
the generator's output, that every change names a rule, the limits, and
that the generator's source names none of the five held-out lines.

## The new baseline (stage 1)

Stage 1 built checks 7 to 22 and ran them on Oxide's lists before writing
any list; check 23 came with the generator. The baseline is the Oxide
column above. Checks 2 and 3 on Oxide's lists are the scoring track's
(`~/oxide-trials/learnset-baseline/checks-2-3.md`): of 86 lines that met a
boss in their window, 38 were taken by none (leads, not verdicts) and 20
by every boss that met them.

## How the checks read the rules

Every check reads the lists as the player meets them, by the capture rule
and on-time evolution (the step 1 baseline's "How the checks read the
data"). A line is walked from its earliest catch, down every branch.

- **Moves no list may rely on.** The rampage moves (R9, until they are
  one-turn), the moves waiting on Ian's rework (Fury Cutter, Psywave, the
  two-turn attacks that are neither setup nor Solar Beam and Solar Blade,
  every multi-hit move), the moves leaving the game (Fury Attack, Feint, the
  first cut of 2026-09-27, Splash, Teleport, Steel Roller, Ice Spinner),
  R24's moves, fixed and level damage, and status moves whose effect the
  engine does not carry out. None counts toward any check, check 1
  included. Moves for trainers only (R26) do not count toward R1 or R2.
- **Check 7, R1.** The moves by the first split's cap that count, on the
  best catch and branch in that split. Filler is a move Ian rated bad or a
  plain Normal attack of 40 or less on a Pokemon that is not Normal.
- **Check 8, R2.** The new moves a stage learns in each split it is held
  at the cap: from the split after it is had, until the split it evolves in
  by level; through the split after its item comes in reach, if it evolves
  by an item; to the League, if it is final; and from three splits after its
  item, if an item made it final (R10).
- **Check 9, R4.** The first coverage attack (not of the holder's types,
  not Normal, 40 or more by effective power, on a stat at least 80% of the
  holder's better attacking stat, R15).
- **Check 10, R5.** Distinct coverage types the final form has by 78
  (attacks of 50 or more, fitting the final form), Kaizo's types beside.
- **Check 11, R6.** An entry learnt while a stronger, at least as accurate
  move of the same type and class is had, where the entry has no secondary
  effect and no priority.
- **Check 12, R7.** Ian's tiers, by move and by class; a status move he has
  not rated takes the Generation 9 list's tier a step down.
- **Check 13, R8.** A free hold, or one move on both lists at two levels
  inside one split.
- **Check 14, R11.** Each of a stage's types has an attack within a split
  of the stage being had, exempt where check 1 exempts.
- **Checks 15 to 23.** Baton Pass needs a stat-raising move on the line;
  R24's and the removed moves on any level-up entry; an entry below the
  lowest level the stage can be had at, learnt by no earlier stage; a setup
  move beside an attack it boosts by the next split; attacks under 90%;
  known-move evolutions; a move from 61 on each final form; list hygiene;
  a newer move on every line.

## Three corrections to the catch data

Ian named the first two in the insight sessions; the third is his ruling of
2026-09-30. The checks and the generator apply all three; the pool the
stored scores read is left alone, so the census still owes them.

- Amity Square's table has no map header, so no one can meet it: its 16
  catch rows are left out (Swablu is first caught on Route 210 in
  Maylene's split). The encounter track owns wiring or explaining it.
- Cynthia's Togepi egg is received in Fantina's split, after the Eterna
  building, not in Gardenia's.
- The Mining Museum revives fossils only after Cycling Road, so the four
  fossil lines the pool left out come in Fantina's split.

# The learnset rewrite (step 4)

Step 4 of `docs/oxide/learnset-checks.md`: the locked rules of
`learnset-insights.md` become checks and a generator, and the generator
rewrites every level-up list. The branch is `balance-learnset-rewrite`, cut
from `oxide` at da6b92496c (Poison Fang landed). Step 5's exam judged the
first loop's lists; the second loop answers its verdicts, and the branch
lands once the Overseer has read it.

## Summary (2026-10-06, the second loop done)

**Outcome.** The second loop answers the exam. Ian's verdicts on the four
lines that missed, and the reviewer's nine regressions, became general
rules in the generator and the checks; no rule names an exam line except
Ian's own exception for Eevee. The generator rewrote the level-up lists of
617 of the 653 species again from Oxide's lists, with 3,587 changes, each
naming its rule. Every check passes or improves on the first loop, and
both test suites pass (17 of 17 and 5 of 5). Lists average 16.0 entries on
the species the player can own, up from 13.9. The ROM builds. The B3 and
B6 scores were recomputed on these lists, and a second pass verified all
1,030 with no disagreement. As in the first loop, no story fight moves on
Ian's fight scale and no ordinary trainer changes band; only the Hikers
Damon and Maurice pair moves (4.2 to 3.4). The boss readings of step 15
stay the real check of the lists' power.

| Check | Oxide | First loop | Second loop |
|---|---|---|---|
| 7, R1: five moves in the first split (203 lines) | 68 | 8 | 4 |
| 8, R2: two new moves per eight levels held (454 stages) | 272 | 218 | 117, 82 of them only from 61 on |
| 9, R4: coverage by the second split (203) | 106 | 7 | 1 (Unown) |
| 10, R5: three coverage types over the game (226) | 219 | 7 | 4 |
| 12, R7: a good utility move early (226) | 98 | 11 | 1 (Unown) |
| 22: list hygiene, trainer moves off wild catches, False Swipe early, at most two recovery moves | 124 | 18 | 0 |
| 24: branches within 80% of each other where the player chooses (16 choices) | 6 | 8 | 0 |

The exam's lines, read again as a regression check (not a fresh exam):

- **Skorupi.** Knock Off sits at 29, the catch level, so every catch knows
  it. Drapion learns Fire, Ice and Thunder Fang by level-up at 45, 53 and
  63, where Oxide had them only at level 1. Gunk Shot is on neither list.
- **Eevee.** Each stone form has its own list from 20, with no quiet
  splits after the stone. Leafeon, Glaceon and Sylveon evolve by level in
  Oxide (30, 30 and 32), so their lists start there. Last Resort, Moonlight,
  Mean Look, Morning Sun and Confuse Ray no longer sit on every branch;
  Quick Attack stays on all eight as a priority move. No list carries more
  than two recovery moves, and Baton Pass is off Eevee.
- **Koffing.** Haze and Memento are off the player's lists, and no wild
  Koffing knows Destiny Bond or Self-Destruct; they moved to Koffing's egg
  list, the trainers' palette. Weezing gains Shadow Ball, Psybeam, Play
  Rough, Flamethrower and Dark Pulse, and the two branches pass parity.
- **Treecko.** A catch at 9 knows Pound, Dragon Breath and Giga Drain, so a
  Grass attack comes between Absorb's place and Leaf Blade. False Swipe
  and Detect are gone. Fury Cutter stays on Grovyle, counted by no check,
  until Ian's rework ruling lands.
- **Scorbunny** (passed): Raboot's Acrobatics at 17 is gone, read now at
  the 110 power it hits for with no item.

**Ian's action items**, each set out below:

1. The open questions of the first loop still stand where the second loop
   left them: the move reworks, the named cases, and staple coverage
   (question 4, with the new screen's numbers).
2. Say whether check 8's late shortfall is acceptable: 82 stages miss a
   new move only in bands from 61 on, where no move passes the fit bar.
3. Nothing else waits on him before the Overseer lands the branch.

**Next steps.**

| Step | What | Who | About how long |
|---|---|---|---|
| Landing | The branch onto `oxide` with `merge-branch.sh` | Overseer | under an hour |
| Reworks | The engine side of Ian's rework rulings, Upper Hand, Shell Trap and Burning Jealousy among them | a cloud job | a session |
| TM pass | Rerun on the new lists, with the reward table and gauntlets | Balance Agent | 2 to 3 hours, then 2 to 3 to write it in |
| 15 | The bosses read against their bands, once on the QA ROM | Scoring Agent | hours of machine time |

## The second loop: what changed and why

The Overseer relayed Ian's go and seven general rules from the exam on
2026-10-06, then Ian's verbatim verdicts on the four lines that missed. The
exam file itself was not opened in this session, as Ian's first
instruction to it said. Each verdict became a rule over every list:

1. **Item evolutions.** A stone form's list works from the earliest level
   the player can evolve it at. The player levels a stage while its stone
   is out of reach and evolves it at the cap before the stone's split, as
   before; Eevee is Ian's exception ("eevee will almost certainly be kept
   at 20 until it is ready to be evolved"), so its stone forms learn from
   20, with no quiet splits after the stone (R10 set aside for this line).
2. **Strong moves below a catch.** A strong move below the lowest catch
   that the catch does not know moves to that level or just after, where
   the ceilings hold it. The ceilings bind only the moves the generator
   adds or moves; Oxide's existing entries stay where they are (the
   Overseer's correction of rule 2, 2026-10-06).
3. **Branch parity** (check 24). Where the player chooses between a
   stage's evolutions, each branch's best four moves by the cap of that
   split are worth at least 80% of the strongest branch's. A weaker branch
   gets the fitting move that adds most, inside the ceilings.
4. **Trainer moves.** A trainer-only move (Destiny Bond and the moves that
   knock their user out) goes to the line's egg list, the trainers'
   palette, never a wild catch's four moves. 29 egg lists changed.
5. **Working moves only.** Upper Hand, Shell Trap and Burning Jealousy are
   off the lists until the rework job builds their conditions.
6. **Fit.** At most two recovery moves a list, and one added only where
   the line has none. An attack uses the line's better attacking stat; an
   off-stat one fills only an early gap (a type with no attack, or no
   usable same-type attack, in the first two splits). A move added only to
   fill a count must fit well, and no sibling branch shares one. Links are
   read by branch, so one Eeveelution's Moonlight is no reason for
   another's. False Swipe comes by Fantina's split or not at all.
7. **Spread.** R2 counts new moves per band of eight levels, not per
   split, at most three new moves a split (four for a move a rule makes
   due), and lists fill from the front. The R8 changes inside one split
   are dropped; check 13 is for information.

The reviewer's regressions each have a rule now: a catch knows three
counted moves where its first split adds any (Treecko at 9); Acrobatics
reads at double power, since fights carry no items (Raboot); Last Resort
and the other attacks that need a rare condition no longer count as a new
move; Baton Pass needs a boost on the holder's own line (Eevee); and an
attack weaker than a held one with the same effect goes (Mega Drain after
Giga Drain). Coverage over the game (R5) is now due on a final form, which
the bands no longer prompted.

Four gate entries change with the loop, so the integration gate reads the
authored lists as intended: `verify_narcs.py` declares every member of
the learnset archive diverged, `import_base_rom.py` leaves every level-up
list alone on a re-import, the gate runs `test_learncheck` and
`test_learnrewrite` with the other balance suites, and the encounter
track's `test_m8` takes Ditto as its sample of a species vanilla still
agrees with, in place of Bulbasaur, whose list the rewrite changed (Ian's
approval, relayed by the Overseer, for that one change in the encounter
track's files).

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

Ian settled R2 after the exam (2026-10-06, relayed by the Overseer): new
moves are counted per band of eight levels a stage is held through, two a
band, at most three new moves a split, and a move added only for the count
must fit the line well. In the second loop only five bands that start
before Byron's split run short. The rest are late: 80 short bands start in
the League's split, 31 in the Galactic split, 29 in Volkner's and 25 in
Barry's, and 82 of the 117 stages that fail miss only from 61 on. There no
fitting move is left, and the generator leaves the band short rather than
add filler. Every final form keeps a real move from 61 on, which the
rewrite meets on all 226.

Recommendation: accept the late shortfall.

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
- **Wooloo, Abra and Nosepass** fall one or two moves short of R1's five
  in Roark's split. Wooloo's natural second move, Double Kick, waits on the
  multi-hit ruling. Abra's list was Teleport alone, and the rewrite gives
  it Round, Calm Mind and Confusion, all known by a catch at 4. Nosepass
  has four, Tackle among them, and nothing else that fits passes the
  ceilings and the fit bar. Recommendation: accept them until the reworks
  land.
- **Coverage:** Magnezone and Relicanth reach two coverage types and
  Pheromosa one (Kaizo gives them one, two and none). Articuno learns no
  move from after Generation 4: nothing newer fits it by level-up.
  Recommendation: accept all four.
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
few staple moves. Among the screened team members of the second loop,
Bulldoze is known by 948, Rock Tomb by 785, Bite by 585, Earthquake by 545,
Iron Head by 510 and Ice Beam by 406 (the first loop: 896, 922, 553, 588,
618 and 545), so the fit rules eased it a little without changing the
picture. Earthquake was already the screen's top pick on Oxide's lists,
but Rock Tomb, Body Press and Iron Head are new near-universal picks,
which check 3 ("no universal moves") sets against. The generator
can weigh a move down by how many lines already have it, which spreads
coverage over the types' other moves (Smack Down, Rock Slide and Stone
Edge's accurate kin; Mud Shot and High Horsepower; Flash Cannon and Steel
Wing). Recommendation: yes, before the rewrite lands. It changes lists, so
the scores and checks run again (about an hour of machine time), and the
exam is read on the new lists.

### 5. Two notes for the TM pass

R5's coverage by level-up draws most on staple TM moves: in the second
loop Bulldoze is new on 65 lines' lists, Rock Tomb on 47, Throat Chop on
42, Ice Beam on 37, and Earthquake and Shadow Ball on 34 each. The TM pass, which makes TMs single-use, should count
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

| Check | Oxide | First loop | Second loop |
|---|---|---|---|
| 2. Lines met by a boss in their window that no boss takes, of 86 (leads, not verdicts) | 38 | 36 | 35 |
| 2. Lines every boss that met them takes | 20 | 18 | 17 |
| 3. Moves known by a screened member, never picked | 134 of 433 | 173 of 442 | 157 of 427 |
| 3. The screen's most-picked moves | Earthquake, Tackle, Take Down, Crunch, Brave Bird | Earthquake, Taunt, Rock Tomb, Body Press, Iron Head | Earthquake, Taunt, Body Press, Rock Tomb, Iron Head |

The first loop's screen output is kept in
`~/oxide-trials/learnset-rewrite/loop1/`.

The screen takes about the same lines with either version, since it ranks
by stats and type matchups first. It now picks real moves where it picked
filler (Tackle, Growl, Fury Attack and Double Team were among Oxide's top
twenty picks), and more moves go unpicked because the lists are longer
and the screen takes one attack of each type. The staple coverage is
question 4 above.

The rewrite column is the second loop's lists.

| Check | Rule | Oxide | Rewrite |
|---|---|---|---|
| 1 | An own-type attack of 50 within a split (454 stages) | 60 fail, 21 with none by 78 | 0 fail |
| 4 | Fixed or level damage by Gardenia's end; one-hit KO moves | 5; 28 | 3; 0 |
| 5 | Ian's move rules (move data, the same in both) | 14 stat-lowering moves off their PP rule | the same |
| 7 | R1, five moves by the first split's cap, at most one filler (203 lines) | 68 fail | 4 fail: Abra, Nosepass, Unown, Wooloo |
| 8 | R2, two new moves per band of eight levels a stage is held through (454 stages) | 272 fail | 117 fail, 82 of them only in bands from 61 on |
| 9 | R4, the first coverage move by the second split (203 lines) | 106 fail | 1 fail (Unown) |
| 10 | R5, three coverage types over the game (226 final forms) | 219 fail | 4 fail: Magnezone, Pheromosa, Relicanth, Unown |
| 11 | R6, no move dominated by a stronger one already had | 4 entries | 0 |
| 12 | R7, a good utility move by the second split (226) | 98 fail | 1 fail (Unown) |
| 13 | R8, choices inside one split, for information since 2026-10-06 | 274 pairs | 245 pairs |
| 14 | R11, an attack of each of the stage's types within a split (454) | 85 fail | 0 |
| 15 | R21, Baton Pass only with a boost on the holder's own line | 4 species | 0 |
| 16 | R24 and the removed moves off every level-up list | 218 entries | 0 |
| 17 | R25, no move below the level a stage is first had at | 129 entries | 0 |
| 18 | R32, a setup move only beside an attack it boosts | 24 entries | 0 |
| 19 | R37, no attack under 90% accuracy | 165 entries | 16 |
| 20 | Every evolution needing a known move reachable by level-up (10) | 1 fails: Sylveon | 0 |
| 21 | A real level-up move from 61 on each final form (226) | 156 fail | 0 |
| 22 | Hygiene and fit: one move a level, none past 78, no move twice, no trainer-only move in a wild catch's four, False Swipe by Fantina's split, at most two recovery moves | 124 entries | 0 |
| 23 | R16, a move from after Generation 4 on every line (203) | 145 fail | 1 fail (Articuno) |
| 24 | Branches within 80% of the strongest where the player chooses (16 choices) | 6 fail | 0 |

Every catch knows an attack at capture in the rewrite; nine species had a
catch that knew only status moves on Oxide's lists. Sylveon is reachable:
Eevee now learns Charm by level-up, by the general rule that a move an
evolution needs is learnable, with no look at Eevee in particular.

`PYTHONPATH=. python3 -m tools.oxide.balance.learncheck rules` prints every
failure by name, `summary` checks 1, 4 and 5, and `sheets` writes the
split sheets in `docs/oxide/learnset-sheets/`, which now set the rewrite
beside Oxide's lists for reading by split.

## How the generator works

`tools/oxide/balance/learnrewrite.py` (`plan`, `write`, `show SPECIES`) starts
from each list as it was and changes only what a rule asks for, in four
passes. Its log, `tools/oxide/balance/learnrewrite_log.tsv`, has every change
with its rule.

1. **Clean.** The moves leaving player lists or the game go (R24, Fury
   Attack, Feint, the first cut, the dead weight, Ian's useless and
   terrible moves, the moves that call a random move, and the three whose
   condition the engine lacks); a move good only for building a trainer's
   fight goes to the line's egg list, the trainers' palette (R26); a
   phazing move stays only where a wild catch knows it (R18); False Swipe
   goes after Fantina's split; an attack under 90% gives way to an
   accurate one of its type (R37); a rampage move sits where its one-turn
   worth fits (R9); nothing stays past 78. Then a strong move below a
   first stage's lowest catch, which that catch does not know, moves up to
   the catch level.
2. **Structure.** A move below the level a stage is first had at moves
   onto the pre-evolution's list where that species can learn it, else up
   to the stage's level (R25), in both cases where the ceilings hold it;
   an evolution that needs a known move gets the move by level-up. Eevee's
   stone forms drop the copies of Eevee's list that count for nothing.
3. **Fill.** Each line is walked from its earliest catch. The first split
   is filled to five moves with little filler (R1), the catch knowing three
   where the split adds any; each band of eight levels a stage is held
   through gets two new moves (R2), at most three new a split; and each
   addition is the best candidate for what the line lacks by then: an
   attack of each type (R11), a same-type attack of 50 (check 1), coverage
   by the second split and three types over the game (R4, R5), a good
   utility move (R7), a strong same-type attack on the final form (R30), a
   newer move (R16), a late move. Candidates are every working move Oxide
   has, scored by fit: its type and the stat it uses (R3, R15), the line's
   abilities (R31) and stats (R17), and a link to the holder's own branch
   in Oxide's lists, canon or Kaizo, which counts in its favour (more for
   coverage the line otherwise gets only from the relearner). A move that
   answers nothing due must fit the line well, needs such a link, and is
   never one a sibling branch got for the same reason; a status move always
   needs a link. An added attack keeps under a power ceiling for its split
   (60 in Roark's, 75 in Gardenia's, 80 in Fantina's, 90 to Wake's, 100 to
   Candice's, more after; a strong line a split later, coverage lower),
   uses the line's better attacking stat but for an early gap, adds
   something over the line's moves of its type (R6), and is never under
   90% (R37); a utility move keeps under a tier ceiling (good in Roark's
   split, incredible in Gardenia's, fantastic in Fantina's), and a recovery
   move comes only to a line with none. Lists fill from the front. Then
   branch parity (check 24), R19's delay demons and a settle pass (R21,
   R32, R6, R25 again), and the first split once more.
4. **Tidy.** One move a level, no move twice, at most 34 entries (the
   engine's limit), every catch knowing an attack, no wild catch knowing a
   trainer-only move.

A line the player cannot own (the post-game legendaries, the lines no
table reaches) gets the clean and the tidy only. `test_learnrewrite.py`
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
  R24's moves, fixed and level damage, status moves whose effect the
  engine does not carry out, and Upper Hand, Shell Trap and Burning
  Jealousy, whose condition it lacks. None counts toward any check, check
  1 included. Moves for trainers only (R26) and attacks that need a rare
  condition (Last Resort, Dream Eater) do not count toward R1 or R2.
  Acrobatics reads at double power, since fights carry no items.
- **Check 7, R1.** The moves by the first split's cap that count, on the
  best catch and branch in that split. Filler is a move Ian rated bad or a
  plain Normal attack of 40 or less on a Pokemon that is not Normal.
- **Check 8, R2.** The new moves a stage learns in each band of eight
  levels it is held through (two a band, one in a closing band of four to
  seven levels). It is held from the split after it is had, until the
  split it evolves in by level; through the split after its item comes in
  reach, if it evolves by an item; to the League, if it is final; and from
  three splits after its item, if an item made it final (R10). Eevee's
  stone forms are held from the level they arrive at, and Eevee itself is
  held at its level (Ian's exception). A stage waiting on its item is
  levelled to the cap before the item's split, Eevee excepted.
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
  inside one split; for information only, since such a choice costs the
  player nothing (2026-10-06).
- **Check 14, R11.** Each of a stage's types has an attack within a split
  of the stage being had, exempt where check 1 exempts.
- **Checks 15 to 23.** Baton Pass needs a stat-raising move on the
  holder's own list or one it carries from what it evolves from; R24's and
  the removed moves on any level-up entry; an entry below the lowest level
  the stage can be had at, learnt by no earlier stage; a setup move beside
  an attack it boosts by the next split; attacks under 90%; known-move
  evolutions; a move from 61 on each final form; list hygiene and fit (no
  trainer-only move among a wild catch's four, False Swipe by Fantina's
  split, at most two recovery moves); a newer move on every line.
- **Check 24, branch parity.** For each stage the player can evolve two or
  more ways, at the cap of the split by which every branch is open, the
  worth of each branch's best four moves: an attack's effective power with
  the same-type bonus and its share of the holder's better attacking stat,
  a utility move's tier rank times seven. The weakest branch passes at 80%
  of the strongest.

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

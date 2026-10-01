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
- `plscore.py`, `plines.py`, `plkaizo.py`, `plrescore.py`, `ppairs.py`,
  `pboxes.py` and `pdoubles.py`
- their tests: `test_fightsim.py`, `test_plfixes.py`, `test_pline.py` and
  `test_fightai.py` (the AI routine by routine, added 2026-10-01)

The rest of `tools/oxide/balance/` stays the balance track's. The balance
track runs the scorer for its passes and asks this track for any change to
it. The fightai audit, which the Balance Agent had paused, moves here with the
files.

**Ian checks this agent's reasoning** until he is reasonably sure it picks up
the trends the three-gym run found (2026-09-30). Until he says so, every fight
line the agent reaches and every planning idea it adds to the search goes to
him with its reasoning before the agent builds on it. That means the line
turn by turn, why each choice was made, and which of the nine ideas below it
used. A finding he has not checked stays a draft. When the agent pauses for
his check, it tells the Overseer first, in one line.

**Starting the session.** Ian starts it with this prompt:

```
You are the Scoring Agent for Platinum Oxide. Read CLAUDE.md, then
docs/oxide/trainer-scoring-handoff.md, which is your brief and your status
home. Ian checks your reasoning on every line and every new planning idea
before you build on it. Start with step 1 of its order of work.
```

**Where it stands (2026-10-01).** Steps 1 and 2 of the order of work are on
`oxide` (6ce38e1e26): the trainer AI follows `script.s` and `trainer_ai.c`
at HEAD routine by routine, with 365 checks in `test_fightai.py`, and the
simulator's known gaps are filled ("The fightai audit", below). Ian answered
the two questions it raised (his answers of 2026-10-01, below), and step 3
has begun on branch `scoring-step3-bar`, measured against the hand-played
lines rerun on the corrected AI by all three of Ian's numbers (the table
under "The job"). The perfect-line store has been stale since the simulator
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

Make the scorer's line search find lines at least as good as the hand-played
ones, on the same box, and say which planning ideas it needed to get there.
Then use it on the bosses.

The first acceptance check is the three fights below. A line is judged on
three numbers together, never the clean rate alone (Ian, 2026-10-01): the
clean rate (won with no Pokemon fainting), the win rate (won at all) and the
death count (the mean number of the player's Pokemon that faint per fight,
over every fight played). The death count is what separates the gnarliest
fights. The bar is our hand-played lines rerun on the corrected AI, 200 runs
each on the harness's own seeds; the scorer's line must match or beat ours on
the whole of the three, and every report to Ian shows all three side by side.

| Fight | Our line | Clean | Won | Deaths per fight |
|---|---|---|---|---|
| Roark | S12 | 199/200 | 200/200 | 0.005 |
| Mars 1 | S1, the PP stall | 191/200 | 200/200 | 0.045 |
| Gardenia | L1 | 29/200 | 116/200 | 3.325 |

Each figure comes from the harness script's own rows (`compare3.py`,
`mars2.py` and `gardenia4.py` in `~/oxide-trials/three-gym-run/`, whose
`run()` plays every fight to its end and returns whether it was won and how
many of the player's Pokemon fainted), with the variant and seeds the
script's `main()` uses, so the clean rates match the scripts' own output. The
figures before the audit (Roark 199, Mars 1 198, Gardenia 57 clean) were
measured on an AI that got many picks wrong, and no longer count.

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

### Ian's luck budget, and what it does to plans

- **Secondary statuses against the player always land.** Sludge Bomb always
  poisons, Thunder Punch always paralyses, and Confusion always confuses. Plans
  must not rely on dodging them.
- **One crit against the player.** Any plan must survive one crit at its worst
  moment. That is why Steenee hands over after one Play Nice.
- **Everything else rolls at the game's odds**, as the six approved
  assumptions in the balance plan list them.
- **Ties between equal AI picks break at random,** as the simulator does
  (Ian, 2026-09-30). This replaces the earlier wording of the budget, which
  assumed the pick worst for the player.

### The planning ideas that won fights

These are the moves a scorer's search has to be able to make. A one-turn
heuristic does not find them.

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

The lesson is that the scorer needs the planning ideas above as moves in its
search, and fight-level planning (chains of stages through the replacement
map), more than it needs more rollouts.

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

## The harness

The working scripts are in `~/oxide-trials/three-gym-run/`, with a README:

- the rolled box
- each fight's damage table, replacement map and AI-pick probes
- each plan as rules
- the look-ahead player

They are notes for one box and one fight each, not tools. They show how each
answer above was found and give a way to re-check it. Run them from a checkout
of `oxide` at 153d11de2 or later.

## A suggested order of work

1. Finish the fightai audit against the battle-ai docs and the decomp, with a
   test per routine.
2. Fill the known gaps above.
3. Reproduce the three fights. Give the scorer the run's box, and require
   lines at least as good as the table's. Where it falls short, find which
   planning idea it lacked and add it as a move in its search. Each line and
   each new idea goes to Ian for checking before the next step.
4. Play the next bosses with Ian the same way (Jupiter and Fantina, at 33) to
   widen the ground truth before trusting the scorer on bosses it has never
   met.
5. Read each boss over a spread of boxes (answer 3 below), then set the boss
   target with Ian, and hand the scorer to the trainer pass.

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

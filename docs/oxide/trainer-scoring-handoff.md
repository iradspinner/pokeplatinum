# Trainer scoring: the handoff from the three-gym run

This is the brief for the agent that takes over training Oxide's trainer
scorer. On 2026-09-30 Ian and the Oxide Overseer played Roark, Mars 1 and
Gardenia by hand on the fight simulator, as a fresh three-gym run optimised
toward Fantina's cap of 33, to learn what a scorer must know before it can be
trusted. Every mistake along the way was a rule the simulator or the planner
did not have. This document collects those rules, the lines that won, the
simulator's state, and the decisions Ian still has to make.

The scorer's direction is already set in the balance plan
(`docs/oxide/balance-plan.md`, its opening section on the perfect-line
scorer). A fight reads as the clean-win rate of the best line found, with that
line's mean deaths and wipe chance beside it. Bosses are read with a planned
team, ordinary trainers blind. The boss target waits until the scorer reads
Roark sensibly. These three fights are the first bosses with hand-checked
answers.

## The job

Make the scorer's line search find lines at least as good as the hand-played
ones, on the same box, and say which planning ideas it needed to get there.
Then use it on the bosses.

The first acceptance check is the three fights below:

| Fight | Hand-played clean wins | The scorer must reach |
|---|---|---|
| Roark | 199 of 200 | 95% or better |
| Mars 1 | 198 of 200 | 95% or better |
| Gardenia | 57 of 200 (best found) | 28% or better, or a better line than ours |

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
over the charge). Whether 28% for this box says something about Gardenia or
about the box is Ian's call (decision 4).

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
- **Ties between equal AI picks.** The memory of Ian's budget says the pick
  worst for him is assumed, but the simulator breaks ties at random. See
  decision 5.

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

The fixes from this work are on branch `overseer-sim-fixes`, with tests in
`tools/oxide/balance/test_plfixes.py` (24 of 24) and `test_fightsim.py`
(17 of 17). The Balance Agent merged the branch up to b09743ff42 into
`balance-perfectline`. These five later commits wait for its next merge:

| Commit | Fix |
|---|---|
| 0501036640 | Only Thunder Wave among status moves meets the type chart, in the engine and the AI |
| 435f72e6ce | Struggle when no move has PP |
| bbbe4b72a9 | The player's Quick Claw fires (it never did) |
| 095fe2f58c | Powder immunity for Grass types and Overcoat, in the engine and the AI; Leaf Guard in the engine |
| 48ed15ab6b | The switching rules as `TrainerAI_ShouldSwitch` has them, and real types for Weather Ball and Natural Gift |

Earlier on the same branch:

- Magnitude rolls its power.
- Rollout's power is fixed.
- The AI's speed-lowering, Pursuit and Defense Curl routines are corrected.
- Block's trap and Ingrain are tracked.
- Pinch berries fire.
- `BattleAI_PostKOSwitchIn`'s second stage is fixed.

Known gaps, none fixed yet:

- **Fixed-damage moves** have no case. Dragon Rage (40) and Sonic Boom (20)
  fall through to the damage rows at power 1. Ian ruled that Charmander must
  not have Dragon Rage in Roark's split; that ruling is held for the next
  learnset revision.
- **Status moves are not recorded as the move that last hit,** though the
  engine records them. The Natural Cure switch rule then reads 87.5% where the
  engine reads 75%.
- **Oxide's Phase 4 AI catch-up rules** (the table in
  `docs/oxide/battle-ai/README.md`) are mostly unchecked in the port: Big Pecks
  and Mirror Armor, Sturdy in the knockout checks, Queenly Majesty, Bulletproof,
  Purifying Salt and the rest. The Balance Agent's pending fightai audit covers
  them, routine by routine with a test each.
- **Sleep length** in the simulator (1 to 4 turns) is not checked against the
  engine.
- **AI ties** break at random, against Ian's budget. See decision 5.

## The harness

The working scripts are in `~/oxide-trials/three-gym-run/`, with a README:

- the rolled box
- each fight's damage table, replacement map and AI-pick probes
- each plan as rules
- the look-ahead player

They are notes for one box and one fight each, not tools. They show how each
answer above was found and give a way to re-check it. Run them from a checkout
of `overseer-sim-fixes` at 48ed15ab6b or later.

## A suggested order of work

1. Merge the simulator fixes, and finish the fightai audit against the
   battle-ai docs and the decomp, with a test per routine.
2. Fill the known gaps above.
3. Reproduce the three fights. Give the scorer the run's box, and require
   lines at least as good as the table's. Where it falls short, find which
   planning idea it lacked and add it as a move in its search.
4. Play the next bosses with Ian the same way (Jupiter and Fantina, at 33) to
   widen the ground truth before trusting the scorer on bosses it has never
   met.
5. Then set the boss target with Ian, and hand the scorer to the trainer pass.

## Decisions for Ian

1. **Who takes this on.** A new local session (its name and status home), or
   the Balance Agent with this added to its plan.
2. **Whether a win that loses only the planned, least-scaling Pokemon counts**
   for anything in the scorer, or only clean wins count.
3. **The box model for bosses:**
   - one rolled box, as here
   - many rolled boxes, reporting the spread
   - the best box a careful player could build
4. **What Gardenia's 28% means.** Our best line with this box at 26 wins
   cleanly 28% of the time, against 99% at Roark and Mars. Is that the box, our
   planning, or a sign that Gardenia's team is tuned too hard for Fantina's
   split?
5. **AI ties.** The budget in memory assumes the pick worst for the player; the
   simulator rolls them. Which should the scorer use?

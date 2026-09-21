# The encounter tables: authoring pass, handoff plan

Written 2026-09-20 for the agent that will write Oxide's wild encounter tables
from the species pick-list, using the encounter tool as it stands after M4. It
is a plan, not a spec: the design model is `encounter-tool-design.md` (v1.1) and
the tool's state is `encounter-tool-build-plan.md`. This file says what to do,
in what order, with what gate at each step, and which decisions were taken here
so they are not re-decided.

## Resuming cold

> **Added 2026-09-20, after this plan was written.** The tool did not stop at M4.
> M5, the dupe-out planner (`cli plan AREA SPECIES`), and M6, the levels-only
> generator (`cli generate --area AREA --dry-run`), both landed the same day and
> are available to this pass; the build plan's M5 and M6 sections say what they
> do and what to watch for. Where this file says "M5 follows the pass" or "the
> tool as it stands after M4", read M6. Everything else here stands.
>
> **Element 3 landed the same evening (2026-09-20), which collapses this plan's two
> stages into one.** All 159 new species are in the tree at ids 494 to 652, so every
> pick-list line can be placed directly from Step 2 on; the Stage B reservation
> mechanism (decision 1, Step 7) is not needed and should not be built. Coverage now
> runs over 358 species in 177 evolution lines, and `test_step0` / `test_step1`
> were updated to say so. Note the ids are dense after Arceus, not National Dex
> numbers (`docs/oxide/species-id-scheme.md`).
>
> **Step 0 done, 2026-09-20.** M7 (`verify_narcs.py --source`) had landed with the
> tool, so that item was not rebuilt. The gate's numbers, and where the plan's
> 375 / 237 / 61 differ from the audit's per-key counts, are in the build plan's
> "Authoring pass" section. Two things learned there that bear on Step 3: an A5
> head can never hold a top-rung slot (its 40 is the two 20% slots, whatever the
> ladder), and `apply` lays levels out as the plain ladder, so `generate --dry-run`
> is the tool for tuning them afterwards.
>
> **Step 1 done, 2026-09-20.** `order` is on all 185 sidecar areas and `tier` on
> all 360 pick-list rows, both from `cli order-init` and `cli tier-init`, which
> refuse to run again without `--force` so Ian's edits survive. R12 evaluates and
> fails 9 lines on the current tables. The placements the outline left open and
> how the tiers were derived are in the build plan's Step 1 entry. Note for Step
> 2: R12's cost counts land and water tables only, so a line meant to come from
> swarms, radar, dual-slot or honey trees needs a wild home or a scripted source
> as well, or the ceiling raised.

Read, in order: this file; `docs/oxide/encounter-tool-build-plan.md` "Resuming
cold" (run its check commands, they must all pass before anything is touched);
`docs/oxide/encounter-tool-design.md` sections 1, 2 and 7; `CLAUDE.md` and
`docs/oxide/design-doc.md` section 5 for the working rules. This track owns
`tools/oxide/encounters/`, `res/field/encounters/`, `docs/oxide/encounters/` and
the `encounter-*.md` docs. Status for this work goes in the build plan under a
new "Authoring pass" section and in the one encounter paragraph at the top of
the tracker, nowhere else. Work on a worktree branch and merge into `oxide` when
green (`tools/oxide/integrate.sh` does the merge; `/integrate` in the planning
session runs it).

## What the job is

Rewrite every wild encounter table so that the only species a player can meet in
the wild are the ones on `docs/oxide/species-pick-list.csv`, laid out according
to the design model: a level ladder that makes repel manipulation pay, a
concentration arc that makes the early game feel early, route-to-route variety,
and a guaranteed acquisition path for every line on the list. The tool measures
all of that; the linter passing on the finished tables is the definition of done.

### The facts that size it, measured 2026-09-20

- The pick-list has 360 rows: 199 natives, 159 new species (in the tree since
  element 3 landed, ids 494 to 652), 2 cut.
- The current tables (the base ROM's rewrite) use 375 distinct species, and **237
  of them are not on the pick-list**. 183 of the 185 encounter files reference an
  off-list species somewhere; 1,250 of the 2,052 land slots do. Sinnoh staples are
  among the off-list species: Starly, Bidoof, Geodude, Shellos, Burmy, Unown. This
  is therefore a full authoring pass over all 171 live land tables, not an edit.
- 61 of the 199 natives appear in no table today.
- Off-list species also sit in every other encounter key: surf and the three rods
  (about 640 slot references), swarms (226), Poke Radar (440), the five dual-slot
  lists (about 970), and the day/night overrides (about 390). Any of them left in
  place is a leak: a species the list says is unobtainable, obtainable.
- The tool writes land slots, `land_rate`, day/night slots 2-3 and water/rod slots.
  The Pokedex area pages regenerate at build time from the encounter
  sources (`res/field/encounters/meson.build`), so they need no separate work.

## Decisions taken here

Do not re-decide these. Anything marked *Ian* is his to change and the plan says
what to do meanwhile.

1. **Two stages.** Superseded: element 3 landed before Step 2, so every pick-list
   line is placed directly and no reservation mechanism is built (see the banner).
2. **All 171 land tables, in play order, early band first.** Every file has to be
   touched anyway (the leak), so there is no cheaper corridor. But the *order* is a
   corridor: Twinleaf to Eterna first, merged and play-tested, then the rest. The
   design's arc rules (R11) only mean anything over the whole game, so the
   game-wide lint gate is at the end, and the per-corridor gate is per-table rules
   plus Ian playing it.
3. **Availability is accounted by evolution line, and every line gets one home.**
   A home is a table where the line's first stage holds at least 10% (a 20% or 25%
   face, or a 10% slot on a real rung). Cameos elsewhere are what R13 wants, and
   they are where the dupe-out structure comes from. Gifts, trades, the starter and
   fossils count as acquisition paths (`pokemon-gifts.md` has the gifts), so a line
   given away in a house needs no wild home, though it may still cameo.
4. **The sidecar is the design source; the JSON is its materialisation.** Each
   area's entry in `docs/oxide/encounters/design.json` gains `order`, `cast` (the
   species in slot order with their rung), `reserved`, and the existing
   `archetype`, `base_level`, `intent`, `locked`. A new `cli apply` lays out the
   twelve slots from archetype signature plus ladder plus cast and writes them
   through `model.py`, so the JSON is never hand-edited and the style guarantee
   holds. This is design-doc section 8.2 step 3 (the piece the build plan calls
   the highest value per line of code) plus a deterministic slot layout; it is not
   the M6 generator and does not choose species.
5. **Water, rods, swarms, radar, dual-slot, honey trees, Great Marsh, Trophy
   Garden get a no-leak pass only.** Replace each off-list species with an on-list
   one of similar role and level, keep the shapes. Their proper design is a later
   pass; the design doc scoped the first pass to land and the linter is calibrated
   on land. **Amended by Ian, 2026-09-21: surf tables get designed in this pass,
   not only de-leaked**, but a surf table counts as an acquisition path (R12 and
   the availability report) only where the player can actually reach that water.
   Several areas carry a surf table with no reachable water; the sidecar needs a
   per-area flag saying whether the water is reachable, set by reading the map,
   and the audit skips surf tables where it is false. Rods stay a no-leak pass.
6. **Progression order.** *Ian's open question 2.* The agent writes `order` for
   all 185 areas from Sinnoh's actual route sequence (the outline below), commits
   it, and Ian corrects it in the file. Nothing waits on the correction.
   **Ian's review, 2026-09-21:** the committed order is right to his eye with one
   correction, the Old Chateau needs Cut and so comes after Eterna City and Route
   211 west, not straight after Eterna Forest. And a task to add: every area gets a
   `split` in the sidecar, the story gate it sits behind (the badge or HM that
   opens it, so the Old Chateau is in the Gardenia split), so that `order` is
   derived from and checked against the gates rather than eyeballed. Areas within
   one split keep their relative order. Do this in Step 2, where the availability
   plan needs the gates anyway.
7. **Tiers.** *Ian's open question 3.* The agent adds a `tier` column to the CSV
   with a proposed default (`gate` for legendaries, fossils, the starter lines and
   anything scripted; `starter-adjacent` for lines whose first stage can sit on
   Routes 201-205; `preferred` for the rest of the Sinnoh dex; `filler` for the
   remainder), commits it, and Ian edits. R12 runs from the first commit instead
   of reporting itself skipped.
8. **Static encounters and off-list gifts are reported, not changed.** Scripts that
   battle or give a species are outside this track. The leak audit lists any that
   name an off-list species; Ian decides.
9. **Unown and the Solaceon Ruins.** Unown is off-list, so the ruins rooms become
   ordinary cave tables (Stage A gives them a cave cast) and `unown_table` stops
   mattering. **Ian, 2026-09-21: Unown stays off the list.** Settled.
10. **Levels stay close to vanilla's.** The base ROM changed species on 114 of 171
    tables but levels on only 27, and vanilla's ladder is the thing the design is
    copying. `base_level` per area comes from vanilla (`--ref main`), and the
    archetype's ladder sits on top of it. Do not re-tune the level curve.
11. **A line the game hands over with certainty appears in no encounter table
    (Ian, 2026-09-21).** Togepi from Cynthia's egg in Eterna and Riolu from
    Riley's egg on Iron Island are the examples; the rule is any species a script
    gives unconditionally, as opposed to a choice (starter, fossil) or a random
    roll (the base ROM's gift houses). Build the list from `pokemon-gifts.md` and
    the scripts, show it to Ian once, then enforce it as a lint rule (next free R
    number): a guaranteed line is absent from every land, water and rod table, and
    the availability audit reports it as scripted rather than needing a home. The
    tiers and the R12 cost ceilings stay as committed; this is the one change.

## The steps

Each step ends at a gate that can fail. Do not start the next step on a failed
gate; report instead.

### Step 0: tooling, before any table changes

Done 2026-09-20; what was built and the gate's numbers are in the build plan's
"Authoring pass" section.

### Step 1: order and tiers

Done 2026-09-20; see the build plan's Step 1 entry.

### Step 2: the availability plan

From `cli coverage` and the leak table, write `docs/oxide/encounters/availability.md`
(generated by a script, committed): one row per line on the pick-list with its
planned home area, its planned cameos, its non-wild sources, and its tier. Every
line must have a home or a non-wild source. Lines with neither are the design
problem this step solves, on paper, before any slot is written. Respect progression:
a line's first appearance is at or after the point its tier implies.

*Gate:* no line without a source; the early band's cast fits 3-5 species per table
with the lines whose tier says early.

### Step 3: author the first corridor (Twinleaf to Eterna)

Roughly the first 25 areas by `order`, which is most of the early band. For each:
pick the archetype from the band's preferred set (design doc 2.5) while watching
the game-wide budget (2.3); set `base_level` from vanilla; write the `intent` line
first, in one sentence, saying what the table is for; write the `cast` with rungs;
`cli apply`; `cli lint AREA`. Keep the day/night overrides to slots 2-3 and use them
for two species that make the time of day matter. Early tables carry the
`starter-adjacent` lines and nothing above their tier.

*Gate:* every corridor table has 0 lint errors; `report` on the corridor shows early
tables at 3-5 species, top slot 40-50%, HHI 0.35-0.50; merged to `oxide`; Ian plays
Route 201 to Eterna Forest in the emulator and says the routes feel like routes.

### Step 4: the rest of the land tables

Mid band, then late, by `order`. The archetype budget is the constraint that only
shows at the end: after every table has a cast, `lint` game-wide must pass R8
(spread ≥ 2.2), R9 (signatures ≥ 0.35), R11 (arc decreasing) and R12; R13 is the
one to push as far as it goes and report honestly if 4x is not reachable. Use
`report` after each twenty tables to see the spread and the arc forming; if the
spread is stuck, the fix is more A2/A3/A4/A9/A10 tables, not tweaks to A1 ones.

*Gate:* game-wide lint 0 errors; R8, R9, R11, R12 pass; the R13 number and the full
section 6.6 table against the targets in design doc 2.1 are in the build plan's
outcome for this step.

### Step 5: the no-leak pass on everything else

Water, rods, swarms, radar, dual-slot, honey trees, Great Marsh, Trophy Garden:
replace off-list species, keep the shapes. `cli audit` is the check.

*Gate:* `cli audit` reports 0 off-list references outside scripts; the script list
is in the report for Ian.

### Step 6: build, verify, play

`make rom`; `verify_narcs.py --encounters --source` clean; `integrate.sh` clean; Ian
spot-checks a late route and a dex area page in the emulator.

*Gate:* the built ROM's tables are the source JSON, field for field.

### Step 7: reservations for Stage B

Not needed; see decision 1.

## Authoring rules, the short form

The design doc is the authority; these are the ones that bite while writing.

- One face per route: an A1 table has one 40% species and it is the species the
  route is remembered for. Two 20% faces is an A6, and A6 is rationed.
- The rung a species sits on is a decision separate from its weight. Put the
  thing worth a repel on rung 3 or 4, and put a duplicate of a head species up
  there with it so the top rung is 2-4 wide (R6), never a single guaranteed prize.
- Real 1% tails (A5, A10) are for species that pay off a dupe-out plan: something
  the player will have deleted the junk around by then. A 1% species with no junk
  around it is a lottery ticket, which is the old design's mistake.
- Repeat species across tables at *different* positions: 25% face here, 4% tail
  there (R13). Same species at 20% on six routes is Drayano's flatness.
- Early tables (order roughly 1-25): 3-5 species, top slot 40-50%, HHI 0.35-0.50.
  Late tables: 5-8 species, top slot 25-35%, HHI 0.18-0.28. The cast grows as the
  game opens up; that is the arc.
- `intent` is one sentence and is written before the cast. It is what Ian reads
  in six months.
- Never edit the JSON by hand. `cli apply`, `cli set`, or the UI.

## Progression order, the outline to start from

Twinleaf, Route 201, Lake Verity, Sandgem, Route 202, Jubilife, Route 203,
Oreburgh Gate, Route 207 (south), Oreburgh, Oreburgh Mine, Route 204 (south),
Ravaged Path, Route 204 (north), Floaroma, Route 205 (south), Valley Windworks,
Floaroma Meadow, Route 205 (north), Eterna Forest, Eterna, Route 211 (west), Mt
Coronet (1F north), Route 206, Wayward Cave, Route 207, Route 208, Hearthome, Route
209, Lost Tower, Solaceon, Solaceon Ruins, Route 210 (south), Route 215, Veilstone,
Route 214, Maniac Tunnel, Valor Lakefront, Route 213, Pastoria, Great Marsh, Route
212, Trophy Garden, Route 210 (north), Route 211 (east), Celestic, Fuego Ironworks,
Route 218, Canalave, Iron Island, Route 219, Route 220, Route 221, Lake Valor, Route
216, Route 217, Acuity Lakefront, Snowpoint, Lake Acuity, Mt Coronet (upper), Spear
Pillar, Sendoff Spring, Turnback Cave, Route 222, Sunyshore, Route 223, Victory
Road, Pokemon League, then the Battle Zone: Route 225, Survival Area, Route 226,
Route 227, Stark Mountain, Route 228, Route 229, Resort Area, Route 230, and the
post-game lake rooms. Areas with several encounter files (Mt Coronet, Victory
Road, Turnback Cave) take consecutive integers in floor order.

## What to report back to Ian

At each gate, in the build plan's "Authoring pass" section: what was done, the
lint and report numbers against the targets, what could not be reached and why,
and what is waiting on him. In the tracker, only the one encounter paragraph. At
the end: the section 6.6 table (vanilla, old tables, new tables, target), the
availability report's summary line (lines with a wild home / non-wild source /
none), and the leak audit's script list.

## Open for Ian, none blocking

- ~~Corrections to `order` and `tier`~~ done 2026-09-21: see decisions 6, 7 and 11.
- ~~Whether Unown returns to the list and whether surf gets designed now~~ done
  2026-09-21: Unown off, surf designed but counted only where reachable
  (decisions 5 and 9).
- Any off-list species the leak audit finds in scripts.
- Whether the first corridor's feel is right, after playing it (Step 3's gate).

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
> **Step 0 done, 2026-09-20.** M7 (`verify_narcs.py --source`) had landed with the
> tool, so that item was not rebuilt. The gate's numbers, and where the plan's
> 375 / 237 / 61 differ from the audit's per-key counts, are in the build plan's
> "Authoring pass" section. Two things learned there that bear on Step 3: an A5
> head can never hold a top-rung slot (its 40 is the two 20% slots, whatever the
> ladder), and `apply` lays levels out as the plain ladder, so `generate --dry-run`
> is the tool for tuning them afterwards.

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

- The pick-list has 360 rows: 199 natives that exist in the tree today, 159 new
  species that **do not exist yet** (they arrive with Phase 4 step 3, the species
  port), 2 cut. So this pass can only place natives, and has to leave a mechanical
  path for the other 159.
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
  It does not yet write swarms, radar or the dual-slot lists, and it does not read
  `encounters_honey_tree`, `encounters_great_marsh_lookout` or the trophy-garden
  source. The Pokedex area pages regenerate at build time from the encounter
  sources (`res/field/encounters/meson.build`), so they need no separate work.
- Two verification tools assume the tables still match the base ROM and **will
  start failing the moment a table is authored**: `import_base_rom.py --dry-run`
  (its encounter count) and `verify_narcs.py --encounters` (compares the built
  NARC to the base ROM). Both are in `tools/oxide/integrate.sh`. Step 0 fixes
  them before any table changes, or the integration gate breaks on the first
  merge.

## Decisions taken here

Do not re-decide these. Anything marked *Ian* is his to change and the plan says
what to do meanwhile.

1. **Two stages.** Stage A authors every table with natives only and is playable
   as soon as it is merged. Stage B places the 159 new species after Phase 4 step
   3. Stage A records where each new species is meant to go as a *reservation* in
   the sidecar (a slot holding a native placeholder now, and the intended species
   named beside it), so Stage B is a mechanical apply, not a redesign.
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
   on land. *Ian* may want to fold surf into the design earlier.
6. **Progression order.** *Ian's open question 2.* The agent writes `order` for
   all 185 areas from Sinnoh's actual route sequence (the outline below), commits
   it, and Ian corrects it in the file. Nothing waits on the correction.
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
   mattering. *Ian* can put Unown back on the list instead; say so before Step 3.
10. **Levels stay close to vanilla's.** The base ROM changed species on 114 of 171
    tables but levels on only 27, and vanilla's ladder is the thing the design is
    copying. `base_level` per area comes from vanilla (`--ref main`), and the
    archetype's ladder sits on top of it. Do not re-tune the level curve.

## The steps

Each step ends at a gate that can fail. Do not start the next step on a failed
gate; report instead.

### Step 0: tooling, before any table changes

Small additions to `tools/oxide/encounters/`, each with a test in `test_m5a.py`
(or whatever the next test file is called; keep the pattern).

- `model.py`: writers for `swarms`, `radar` and the five dual-slot lists, the same
  `_replace` mechanism as `set_time_slot`. Readers for `encounters_honey_tree`,
  `encounters_great_marsh_lookout` and the trophy-garden source, species only.
- `cli audit`: every species reference in every encounter source, by file and key,
  flagged on-list or off-list, plus the `StartWildBattle` and `GivePokemon` species
  in `res/field/scripts/*.s`. Output is the leak table for Step 2 and the zero
  check for Step 5. Reads the pick-list CSV; the species-name-to-constant mapping
  is `dex.py`'s job (extend it with the reverse of `display_name`).
- `cli coverage`: for every line on the pick-list (families from `dex.py`), where it
  is obtainable: wild home tables, cameos, gifts (`pokemon-gifts.csv`), trades,
  and nothing. This is R12's input made visible.
- `cli apply AREA`: materialise an area from its sidecar entry (decision 4).
  Layout rule: the archetype's signature gives the merged shares; walk the twelve
  slot rates and assign species so each species' summed rate equals its share
  (duplicates fill where a share exceeds one slot's rate); levels are `base_level`
  plus the archetype ladder's offset per slot, non-decreasing by slot index (R1);
  `cast` may pin a species to a rung, otherwise the first-listed species take the
  common head. `--all` applies every area with a cast. `--dry-run` prints the diff.
- `import_base_rom.py`: an `AUTHORED` set (mirroring `bulk_scripts.py`'s `DIVERGED`)
  naming encounter files the importer must not touch; the dry run reports them as
  "authored, skipped" and counts 0.
- `verify_narcs.py --encounters --source`: compare the built ROM's `pl_enc_data.narc`
  against `res/field/encounters/*.json` field by field (this is M7). The existing
  `--ref` mode stays for tables still matching the base ROM.
- `tools/oxide/integrate.sh`: switch the encounters check to `--source`.

*Gate:* M1 to M4 tests still pass; `integrate.sh --dry-run` passes; `cli audit` and
`cli coverage` run on the unchanged tree and their numbers match the facts above
(237 off-list species, 61 natives with no table).

### Step 1: order and tiers

Write `order` into every sidecar entry, write the `tier` column, commit both. Then
`lint --ref main` must show R12 evaluated rather than skipped. On the current tree
R12 will fail loudly; that is the point.

*Gate:* R12 runs; `order` covers all 185 areas with no duplicates.

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

For every new species with a planned home or cameo, a `reserved` entry in the
sidecar naming the slot and the species, and a native placeholder in that slot
chosen so the table still passes lint. After Phase 4 step 3 lands, `cli apply
--reservations` swaps them in and the availability report covers all 358 lines.

*Gate:* every new species on the pick-list has at least one reservation or a
non-wild source noted in `availability.md`.

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
none), the leak audit's script list, and the list of reservations for Stage B.

## Open for Ian, none blocking

- Corrections to `order` and `tier` once the agent's defaults are committed.
- Whether Unown returns to the list (decision 9) and whether surf gets designed
  now (decision 5).
- Any off-list species the leak audit finds in scripts.
- Whether the first corridor's feel is right, after playing it (Step 3's gate).

## Sizing

Step 0 is a day of tool work with tests. Steps 1 and 2 are a session. Steps 3 and
4 are the bulk: 171 casts and intents, perhaps 20 tables a session once the
archetype budget is understood, so about nine sessions, with the corridor merge
after the first two. Steps 5 to 7 are two sessions. The generator (M6) would cut
Steps 3 and 4 but is not needed for them and is not on this plan's path; build it
afterwards if the hand pass shows which parts were mechanical.

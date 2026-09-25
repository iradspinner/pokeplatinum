---
name: author-table
description: How to write or revise a wild encounter table for Platinum Oxide with the encounter tool (cli apply, lint, report, plan, generate, audit, coverage) and the design model's archetypes, ladder and availability rules. Use this whenever a session is editing anything under res/field/encounters/ or docs/oxide/encounters/design.json, working on the encounter authoring pass, placing species on routes, fixing a lint finding, or asked what a route "should feel like", even if the user just names a route and a Pokemon.
---

# Authoring an encounter table

The tool is the only writer of the encounter JSON. It preserves the decomp's
file style, enforces the day/night rule structurally, and every number it
prints comes from one implementation of the maths, so the CLI, the UI and the
linter cannot disagree. Editing the JSON by hand throws all of that away.

The plan for the whole pass is `docs/oxide/encounter-authoring-plan.md`; its
status is the "Authoring pass" section of
`docs/oxide/encounter-tool-build-plan.md`, and each finished step's full entry
is in `docs/oxide/encounter-tool-build-plan-archive.md`. The design model is
`docs/oxide/encounter-tool-design.md` sections 2 and 7. This skill is the
two-screen version for working on one table.

## The commands

All run from the repo root with `PYTHONPATH=.`:

```
python3 -m tools.oxide.encounters.cli show AREA                 # the table now
python3 -m tools.oxide.encounters.cli report AREA               # its metrics
python3 -m tools.oxide.encounters.cli lint AREA                 # its findings
python3 -m tools.oxide.encounters.cli apply AREA --dry-run      # lay out from the sidecar cast
python3 -m tools.oxide.encounters.cli apply AREA                # and write it
python3 -m tools.oxide.encounters.cli generate --area AREA --dry-run   # tune levels for R3
python3 -m tools.oxide.encounters.cli plan AREA SPECIES         # does the acquisition path work
python3 -m tools.oxide.encounters.cli set AREA SLOT --species S --level L   # one slot
python3 -m tools.oxide.encounters.cli audit --summary           # off-list leaks, all files
python3 -m tools.oxide.encounters.cli coverage --status none    # pick-list lines with no source
python3 -m tools.oxide.encounters.cli --ref main report         # vanilla, for comparison
```

`--ref main` reads vanilla; the working tree holds the base ROM's tables until
the pass replaces them. Calibrate against `main`, never the working tree.

## Writing one table

1. Read its sidecar entry in `docs/oxide/encounters/design.json`: `order`,
   `band`, `base_level`, `archetype`, `intent`, `cast`, `locked`, `reserved`.
   `base_level` comes from vanilla; leave the level curve alone.
2. Write the `intent` line first, one sentence: what this table is for and what
   a player remembers it by. If you cannot write it, you do not know the table
   yet. It is what Ian reads in six months.
3. Pick the archetype from the band's preferred set in design doc 2.5, which
   since 2026-09-21 is the cap rather than a concentration arc: A11 to A19 in
   rotation, top slot 25 to 35% in every band. The game-wide budget in 2.3 is
   the constraint that only shows at the end, so check `report` every twenty
   tables: R8's spread floor is 1.8x now (the authored game reads about 1.96x).
4. Write the `cast` in share order: the first entry is the face. Pin a species
   to a rung with `{"species": X, "rung": r}` when the rung is the point of it.
   Two facts about the layout: an A5 head can never hold a top-rung slot (its 40
   is the two 20% slots, whatever the ladder), and A1's 10 and 5 leave room for a
   duplicate of a head species on the top rung, which is where R6's "top rung 2
   to 4 wide" comes from. `apply` refuses a pin the arithmetic cannot honour.
5. `apply --dry-run`, read the diff, `apply`. Levels come out as the plain
   ladder; if `lint` says R3 fails, `generate --area AREA --dry-run` proposes a
   ladder that reaches the uplift, and `generate` writes it.
6. `lint AREA` until it reports no errors, then `plan AREA SPECIES` for the
   species the table exists to deliver: the answer should be a short list of
   earlier routes to dupe out, not "unreachable".
7. Day and night overrides live in slots 2 and 3 only (`set_time_slot` refuses
   anything else). Use them for two species that make the time of day matter.
8. Every pick-list line is placeable: Phase 4 element 3 put all 159 new species
   in the tree (ids 494 to 652), so the plan's Stage B reservations are moot.
   Use the species constant from `docs/oxide/species-id-map.csv` when in doubt.

## Rules that bite while writing

- One face per route. Two 20% faces is an A6, and A6 is rationed.
- The rung a species sits on is a decision separate from its weight. The thing
  worth a repel goes on rung 3 or 4 with a head-species duplicate beside it, so
  the top rung is a small pool, never one guaranteed prize.
- Real 1% tails (A5, A10) are for species that pay off a dupe-out plan. A 1%
  species with no catchable junk around it is a lottery ticket, which was the old
  design's mistake.
- Repeat species across tables at different positions (R13): 25% face here, 4%
  tail there. The same species at 20% on six routes is the flatness the survey
  measured in every challenge hack.
- Every pick-list line needs one home (a table where its first stage holds at
  least 10%) or a non-wild source. `coverage` is the check; gifts and trades
  count (`docs/oxide/pokemon-gifts.md`).
- Off-list species are leaks: the pick-list is the availability list and
  anything else the player can meet contradicts it. `audit --fail-on-leak` is the
  check, over every key (surf, rods, swarms, radar, dual-slot, day/night, honey
  trees, Great Marsh, Trophy Garden), not just land.
- Aspirational rules (R3, R5, R11b, R13) are meant to sit beyond vanilla; do not
  lower a threshold because vanilla fails it. Descriptive rules (R1b, R2, R6,
  R8, R9, R11, R14) must pass on `--ref main`; if one does not, the threshold is
  wrong, not vanilla.

## Ian's rulings from the pass, still in force

These came out of his reviews of Steps 2 to 8 (2026-09-21 and 22). The steps'
full entries are in the build plan's archive; the rules are here so nobody has
to read it.

- Tables are designed per capture area (one location name, however many
  files) and per gym split. The splits, their level caps and the split each rod
  and Surf arrives in are the sidecar's `splits` table; Maylene's cap is 38 in
  the tables and 39 in Ian's sheet, waiting on the balance track.
- A grass table holds eight to sixteen lines with distinct day and night pairs,
  and nothing over 35%.
- A place whose tables sit in one spot is either identical throughout or very
  different part to part, never one pool rotated (Ian, 2026-09-26). The
  sidecar's `groups` table says which: "same" (Solaceon Ruins, Lake Verity, the
  Old Chateau, Iron Island, Stark Mountain, the Oreburgh Mine, Wayward Cave, the
  Ruin Maniac's dig, and Mt. Coronet's B1F, Peak and Mountainside) is one cast,
  shape, level and day and night pair on every table; "distinct" (the Great
  Marsh, the Lost Tower, Victory Road, Oreburgh Gate) gives each part a theme and
  a face of its own and lets two parts share at most two species. Lint's R15
  enforces both.
- Mt. Coronet is five captures, not one: North, South, B1F with North Room 2,
  the Peak climb and the Mountainside, named by the sidecar's `capture_area`.
  Only Victory Road's 1F, 2F and B1F come before the Champion; its three side
  rooms lead to Route 224 and are post-game.
- Roark's split holds only starter-adjacent lines, lines with a scripted
  source, and 4% or 1% tails. Ravaged Path is in Roark's split.
- A gate-tier starter is a cameo or a tail, never a home. A delay (a location
  whose halves fall in different splits) must be worth delaying for: several
  starters or value lines at 10 to 20%, not a 5% tail.
- A line fully evolved by level-up under a split's cap belongs in or before
  that split. The availability gate's cap-candidates list must be empty.
- When a table cannot be filled from the pick-list, stop and propose additions
  to Ian before pushing; do not pad it.
- After any change to a table's levels, run `cli evolve`: it puts the stage a
  level deserves in each slot (friendship judged at 20, a stone at 30, a trade at
  38, `BRANCH` in `evolve.py` for a split line), writes the sidecar, and `apply`
  then writes the tables. It has converged when it reports 0 moves.
- Swarms, the Poke Radar, the dual-slot lists and the Trophy Garden dailies are
  not used in Oxide. They are filled with on-list species only so that nothing
  off-list can be rolled, and no capture is counted from them.
- Anything post-champion (Turnback Cave) is out of scope. Scripted gifts are
  even-odds pools per source, one flag each, recorded in
  `docs/oxide/encounters/scripted-sources.md`.
- After any table change, regenerate the sources catalogue:
  `PYTHONPATH=. python3 tools/oxide/pokemon_sources.py`.
- A new way of authoring a table (a sidecar key, a file kind) extends
  `authored_encounters()` in `import_base_rom.py` and `test_step0`'s mirror of
  it in the same commit, or the importer's dry run reverts the table.

## When a batch is done

`cli evolve` reports 0 moves; `cli availability` passes with no cap
candidates; `lint --ignore R12 --fail-on error` is clean (R12's 27 errors are
the legendary pool's lines, which wait on script work); `audit --fail-on-leak`
exits 0; the ROM is built (on GitHub with `tools/oxide/fetch-rom` until the
replacement CPU is in, otherwise `make rom`) and `python3
tools/oxide/verify_narcs.py --built <rom> --encounters --source` reports all 184
tables matching their JSON. The numbers from `report` go into the build plan's
"Authoring pass" section against the targets in design doc 2.1; the tracker's
encounter paragraph changes only if what is live changes, and nothing else in
the tracker is touched.

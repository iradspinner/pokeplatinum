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
`docs/oxide/encounter-tool-build-plan.md`. The design model is
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
3. Pick the archetype from the band's preferred set (design doc 2.5): early
   tables want A1, A3, A4, A9, A10 (3 to 5 species, top slot 40 to 50%); mid A1,
   A5, A6, A9; late A1, A5, A6, A7, A8 (5 to 8 species, top slot 25 to 35%). The
   game-wide budget in 2.3 is the constraint that only shows at the end, so check
   `report` every twenty tables: if the spread is stuck under 2.2, the fix is
   more concentrated tables (A2, A3, A4, A9, A10), not tweaks to A1 ones.
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
8. Stage B reservations: a new species that does not exist yet (the 159 arrive
   with Phase 4 element 3) gets a `reserved` entry naming the slot and the
   species, with a native placeholder in the slot so the table still lints.

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

## When a batch is done

`lint --fail-on error` clean; `make rom`; `python3 tools/oxide/verify_narcs.py
--built build/pokeplatinum.us.nds --encounters --source` reports every table
matching its JSON; the numbers from `report` go into the build plan's
"Authoring pass" section against the targets in design doc 2.1; the tracker's
encounter paragraph is updated and nothing else in the tracker is touched.

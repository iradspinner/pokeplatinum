# The encounter tool: a build plan

Written 2026-09-20, from `docs/oxide/encounter-tool-design.md` (v1.0) and the
measurements in `docs/oxide/encounter-design-survey.md`, both of which are now
repo-tracked rather than living only in the project folder's `Claude outputs`.

The design doc says *what* the tool is and *why* each number in it is the number
it is. It does not say in what order to build it, what the repo already provides,
or which of its claims survive contact with the files on disk. This does.

## The short version

Seven milestones, each ending at a check that can fail. M1-M3 are the engine and
are worth building even if the UI never happens, because the CLI alone answers
the question "is this set of tables any good". M4 is the UI. M5-M7 are the
generator, and they are the part most likely to be cut or deferred.

| | Milestone | Ships | Gate |
|---|---|---|---|
| M1 | Round-trip I/O ✔ | `model.py`, `cli.py` skeleton | 185 files load and save with a zero-byte diff — **passed** |
| M2 | Analysis engine | `analysis.py`, `cli report` | Monte-Carlo agreement on repel; survey numbers reproduced from vanilla |
| M3 | Linter | `lint.py`, `cli lint` | Vanilla passes the rules calibrated on vanilla |
| M4 | UI | `server.py`, `ui/index.html` | Edit in the browser lands as the right one-key git diff |
| M5 | Dupe-out planner | `plan` in `analysis.py`, `cli plan` | One hand-verified multi-step plan |
| M6 | Generator | `generate.py`, `cli generate` | A generated band passes lint without hand repair |
| M7 | ROM verification | acceptance harness | Built ROM's NARC matches the source JSON |

## What the repo already gives you

Not starting from zero. Four things exist and should be used rather than
rewritten.

| Asset | Where | What it does for this |
|---|---|---|
| Encounter JSON | `res/field/encounters/*.json` | 185 files: 183 land tables, of which 171 are live. This *is* the tool's state; there is no database to build |
| `jsonstyle.py` | `tools/oxide/` | `replace_value` / `get_value` by key path, on text, preserving the decomp's unreproducible formatting. M1 is mostly wiring this up |
| `verify_narcs.py --encounters` | `tools/oxide/` | Already reads `pl_enc_data.narc` and compares against source. M7 is an extension of it, not a new thing |
| Pinned vanilla | `~/roms/vanilla.nds`, and `git show main:res/field/encounters/…` | The calibration corpus. See the warning below — this matters more than it sounds |

**The vanilla corpus is on `main`, not in the working tree.** The `oxide` branch's
`res/field/encounters/` holds the *base ROM's* 125 rewritten tables, imported
2026-09-20. Every calibration check in the design doc's section 11 — the survey
numbers, the linter sanity pass — has to read `main`'s copies, not the checked-out
ones. Build that in from the start: `--ref main` on the CLI, resolved through
`git show`, defaulting to the working tree. Getting this wrong means calibrating
the tool against the tables it was built to replace.

Measured once the loader could read both (M1): the two corpora differ in **species
on 114 of 171** tables but in **levels on only 27**. The base ROM's encounter
rewrite swapped what you meet and left vanilla's level ladder largely standing, so
the repel structure the design model is built around is still mostly present in the
checked-out tables. That is a better starting position than the design doc assumes,
and it means an early pass could rewrite species against an inherited ladder rather
than building both at once.

## One finding that changes the design doc

R1 as written does not survive the files.

> **R1 (error) — Ladder monotonicity.** Slot levels are non-decreasing with slot
> index. […] the single highest-leverage rule in this document.

and acceptance criterion 6 says vanilla must pass R1. Measured over all 171
vanilla land tables:

| | |
|---|---|
| Levels non-decreasing by slot index | **20 of 171 (12%)** |
| Tables with exactly 4 distinct levels | 136 of 171 (80%) |
| Rarity-vs-level Spearman, median | **+0.68** (p10 -0.06, p90 +0.98) |
| Tables with positive correlation (>0.1) | 150 of 171 (88%) |
| Tail slots 8-11 averaging above head slots 0-1 | 153 of 171 (89%) |

Vanilla Route 201 is the clean counter-example: levels `2,2,3,3,3,3,3,3,2,2,2,2`.
The 1% Growlithe slots sit at the table's *minimum* level, so a repel at 3 deletes
them rather than isolating them.

The survey's ladder claim was always about the *median* offset per slot across
171 tables, and that claim holds — the census, the 4-rung count and the
correlation all confirm it. What does not hold is the per-table strict form. So:

- **Keep R1 as an error for Oxide-authored tables.** It is a house rule and a good
  one; the generator assigns levels this way in step 3, and a hand-edit that breaks
  it is almost always a mistake.
- **Do not check R1 against vanilla.** Drop it from criterion 6, which otherwise
  fails 88% of the corpus on day one and invites someone to "fix" the threshold.
- **Add R1b (warn), the vanilla-calibrated form:** rarity-vs-level Spearman ≥ 0.5.
  Vanilla medians 0.68. This is the rule that can be pointed at both corpora.

Everything else in section 11 looks sound and the 171-table count reproduces
exactly, which is a good sign for the survey's other numbers.

## The milestones

### M1 — Round-trip I/O — **done, 2026-09-20**

`model.py`: load an area (decomp JSON text + parsed view + sidecar entry), write a
slot back through `jsonstyle.replace_value` at
`land_encounters[i].level` / `.species`, never re-serialising the file.
`cli.py` gets the argument skeleton and `--ref`.

The sidecar `docs/oxide/encounters/design.json` is created here, initially with an
entry per area carrying only `band` (derived from median level) and an empty
`intent`. Archetype assignment waits for M2, which is what can measure fit.

*Gate:* load all 185, write every one back unchanged, `git diff --exit-code` clean.
Then the same with one slot changed, and confirm exactly one key moved.

**Outcome.** `PYTHONPATH=. python3 -m tools.oxide.encounters.test_m1` — 13/13, on
both corpora. The round-trip is checked in its strong form: writing raw text back
is trivially clean, so instead every land key is replaced by *the value it already
holds* and the text must come back byte-identical. That exercises the edit path on
all 2,208 slots rather than the parser alone. One slot write moves exactly one line
on all 171 live tables.

The file accounting in the design doc needed sharpening, and it is the thing that
would have bitten a loader. It is not "14 files with no land data": it is **2**
files in a different format entirely (`encounters_great_marsh_lookout`, which holds
binocular data, and `encounters_honey_tree`, which holds three pools) plus **12**
that carry a full twelve slots the game never rolls because `land_rate` is 0. The
two categories fail differently and `model.py` keeps them apart — `has_land` versus
`land_active`. The `[  ]` empty-array style never came up, since no write touches an
empty array.

Two guards worth knowing about, both enforced in the model rather than left to the
linter. An area loaded through `--ref` refuses writes and refuses to save, so the
calibration corpus cannot be edited by accident. And `set_time_slot` refuses
anything outside `day`/`night` slots 2-3, which is R7 made structurally impossible
rather than merely reported.

### M2 — Analysis engine

`analysis.py`, pure functions, rate-array-agnostic from the first line so water and
fishing tables are later a config change: `base`, `rungs`, `pool`, `conditional`,
`throughput`, per-table metrics, per-game metrics. `cli report --json`.

Two rules worth fixing in code now rather than discovering later: `>=` on the repel
comparison, and rung collapsing (four distinct levels that produce three distinct
pools are three rungs, and the UI must say three).

*Gate:* two checks, both from section 11.
1. `pool()` against a brute-force simulation of `RepelPreventsEncounter` over 10⁶
   trials on 20 random tables.
2. `report --ref main` reproduces the survey: median HHI 0.275, p10-p90
   0.170-0.420, 71 distinct signatures, median uplift 5.0x, the slot-offset ladder.
   A disagreement here is a bug in one of the two documents and blocks everything
   downstream.

### M3 — Linter

`lint.py` over M2's output, thresholds read from the sidecar, never hardcoded.
R1-R14 plus R1b. Severity as the design doc has it, with R1 scoped to authored
tables and R12 (availability) stubbed to a warning until the pick-list tiers exist.

*Gate:* `lint --ref main` passes R1b, R8, R9 and R11 on vanilla. If a rule vanilla
was derived from fails vanilla, the threshold is wrong — that is the whole point of
the check, and it has already caught R1 once.

### M4 — The UI

`server.py` on `127.0.0.1:8765`, stdlib only, and `ui/index.html`, vanilla JS, no
build step and no CDN. Three columns as specified: area list with sortable HHI,
twelve-slot editor with merged and ladder views, live analysis panel with the
dupes checkboxes. Write on blur.

Build it against M2's JSON and nothing else — every number on screen is an
`analysis.py` call, so there is no second implementation of the math to drift.

*Gate:* edit a slot in the browser, see it in `git diff` at the right key with no
other key touched.

### M5 — Dupe-out planner

The feature the tool exists for. Exhaustive over subsets of a table's ≤12 species
and the rungs where the target survives; needs a progression order for areas,
which is new data — the sidecar's `band` is too coarse, so add an explicit
`order` integer per area. Output the Pareto front and render the best few as prose.

*Gate:* one hand-verified case, worked out on paper first and then matched.

### M6 — Generator

Steps 1-4 of design section 8: assign archetypes and bands to satisfy the budget,
place species under the hard constraints, assign levels and rungs by hill-climb,
then lint and apply scripted repairs with a log.

Step 3 is, as the doc says, the highest value per line of code here, and it is also
the one that can ship alone: a `generate --levels-only` that leaves species
placement to Ian but builds the ladder under them would be useful on day one and is
perhaps a tenth of the work of the full pipeline. Consider doing that first and
treating full placement as optional.

*Gate:* `generate --band early` produces tables that clear lint without hand repair.

### M7 — ROM verification

Extend `verify_narcs.py --encounters` to compare a built ROM's `pl_enc_data.narc`
against the source JSON field by field, the way the trainer and species carry-overs
were verified. Per design section 8.4: the generator reports success from lint,
and lint reports from disk, and this reports from the thing the game actually runs.

*Gate:* `make rom` after a generated pass, then a clean field-by-field compare.

## Suggested order, and what to cut

M1 → M2 → M3 is one continuous piece of work and should not be split across
sessions if avoidable; M2's gate is what validates M1's parse and M3's calibration
is what validates M2's math. Call it the engine.

After that the order is genuinely optional and depends on what Ian wants first:

- **M4 before M5/M6** if the goal is to start designing routes by hand soon. The
  engine plus the UI is a complete, useful tool; the generator is a convenience.
- **M5 before M4** if the goal is to find out whether the *design model* works. The
  planner run against vanilla answers "does the cascade Ian described actually
  exist in tables of this shape" without any UI at all.

M6 is the only part that can be dropped entirely without losing the point of the
tool, and `--levels-only` recovers most of its value cheaply.

## Open questions for Ian

1. **R1's demotion.** The finding above is a real conflict between the design doc
   and the files. Proposed: R1 error for authored tables, R1b warn at Spearman ≥ 0.5
   for calibration, and criterion 6 amended. Confirm before M3 hardens it.
2. **Progression order.** M5 needs an explicit area order and the sidecar does not
   have one. Is there an existing ordering to reuse, or does it get hand-written
   once into `design.json`?
3. **Species tiers.** R12's availability thresholds need the pick-list's `tier`
   field populated (`starter-adjacent` / `preferred` / `filler` / `gate`). Until
   then R12 stays a warning. This is Ian-only work and gates M3's last rule.
4. **Scope of the first authored pass.** 171 land tables is a lot of hand design.
   Is the target all of them, or a corridor — say the first third of the game — to
   prove the model before committing?

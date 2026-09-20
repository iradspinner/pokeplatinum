# The encounter tool: a build plan

Written 2026-09-20, from `docs/oxide/encounter-tool-design.md` (v1.0) and the
measurements in `docs/oxide/encounter-design-survey.md`, both of which are now
repo-tracked rather than living only in the project folder's `Claude outputs`.

The design doc says *what* the tool is and *why* each number in it is the number
it is. It does not say in what order to build it, what the repo already provides,
or which of its claims survive contact with the files on disk. This does.

## Resuming cold

For a session that has none of the conversation this came out of.

**Where the work is.** On `oxide`, merged there 2026-09-20. If
`git log --oneline | grep "Encounter tool M1"` finds nothing, you are on a branch
that predates the merge and none of the files below exist.

The encounter tool and the Phase 3 script/event carry-over run in parallel on the
same branch and share no files: this track owns `tools/oxide/encounters/`,
`res/field/encounters/` and the three `encounter-*.md` docs, and touches nothing
else. Edits to `tracker.md` and `START-HERE-current-state.md` are the exception,
and they have caused three merge conflicts; keep this track's footprint in those
two files to the single status line each already carries.

**One thing from the other track that lands here.** The base ROM's custom script
command, long unidentified, turned out to be a *Repel prompt*: "Repel's effect
wore off, use another one?", offering Repel / Super Repel / Max Repel and setting
the step counter to 100/150/250. Ian added a feature specifically to make repelling
less tedious, which is direct evidence for how central repel manipulation is to the
game he wants — and it makes the manip loop this tool is built around materially
cheaper to actually play. Worth remembering when weighing R3's uplift threshold:
the cost side of a manip is lower in this ROM than in vanilla.

**Read in this order.** This file for what to do next. Then
`docs/oxide/encounter-tool-design.md` sections 1, 2 and 6 for the model — section 1
is the game's actual repel behaviour and is the part that must not be paraphrased
from memory. `docs/oxide/encounter-design-survey.md` only when a number in the
design doc needs its provenance.

**Run the existing work first, to confirm the ground is solid:**

```
cd ~/pokeplatinum
PYTHONPATH=. python3 -m tools.oxide.encounters.test_m1     # expect 13/13
PYTHONPATH=. python3 -m tools.oxide.encounters.test_m2     # expect 23/23, ~1 min
PYTHONPATH=. python3 -m tools.oxide.encounters.test_m3     # expect 18/18
PYTHONPATH=. python3 -m tools.oxide.encounters.cli --ref main report
PYTHONPATH=. python3 -m tools.oxide.encounters.cli report
PYTHONPATH=. python3 -m tools.oxide.encounters.cli --ref main lint   # 0 errors
PYTHONPATH=. python3 -m tools.oxide.encounters.cli lint              # 1 error, R8
PYTHONPATH=. python3 -m tools.oxide.encounters.test_m4     # expect 46/46
PYTHONPATH=. python3 -m tools.oxide.encounters.test_m5     # expect 13/13
PYTHONPATH=. python3 -m tools.oxide.encounters.cli plan encounters_route_214 growlithe
PYTHONPATH=. python3 -m tools.oxide.encounters.test_m6     # expect 19/19
PYTHONPATH=. python3 -m tools.oxide.encounters.cli generate --band early --dry-run
PYTHONPATH=. python3 -m tools.oxide.encounters.server      # the UI, localhost:8765
```

The `plan` line is the whole design in one command: it should take Growlithe from
3% to 100% by naming five earlier routes to catch on first.

The two reports are the heart of it. The first is vanilla and should read median
HHI 0.275, spread 2.48x, 71 signatures. The second is the tables the project
currently has and should read 0.185, 2.14x, 44 — flatter, less varied, and with the
early/late arc running backwards. **The working tree holds the base ROM's tables and
`main` holds vanilla**; every "does this match vanilla" check reads `--ref main`.

**What exists.** `tools/oxide/encounters/` has `model.py` (loading and slot-level
writing), `analysis.py` (all of section 6's maths, pure functions), `lint.py`
(section 7's rules, every threshold read from the sidecar), `dex.py` (species
names and evolution lines from `res/pokemon/`), `planner.py` (the dupe-out planner,
pure apart from its one loader), `generate.py` (the levels-only generator, pure),
`cli.py` (`areas`, `show`, `set`, `roundtrip`, `sidecar-init`, `report`, `lint`,
`plan`, `generate`), `server.py` plus `ui/index.html` for the browser editor, and
`test_m1.py` through `test_m6.py`. The sidecar is `docs/oxide/encounters/design.json`,
which holds every threshold; the per-playthrough caught record is
`docs/oxide/encounters/caught.json`, gitignored.

**Next milestone: M7**, ROM verification — extend `verify_narcs.py --encounters`
so a built ROM's `pl_enc_data.narc` is compared field by field against the source
JSON. M1-M6 are done and their sections below record what each found; M6 shipped
in its levels-only form, and full species placement is deferred, possibly for good.

**Before running the generator for real, read M6's "one consequence"**: it enforces
R1, most current tables break R1, so it will change almost every table it is
pointed at and a few will pay less than they did. Use `--dry-run` first.

Two inputs still missing, both under "Open questions": a real progression order
(the planner and the page approximate it by encounter level, from one place each)
and a `tier` per pick-list line (gates R12).

**Three decisions already taken**, so they do not need rediscovering. Writes go
through `jsonstyle.replace_value` on file text and never re-serialise a whole file.
The design doc's R1 is amended as described under "One finding" below, accepted by
Ian and implemented in M3. And the doc's thresholds are sorted into *descriptive*
(vanilla must pass; if it fails, the threshold is wrong) and *aspirational*
(deliberately beyond vanilla) — the tags live in `lint.py` and the reasoning is in
M3's outcome. Do not "fix" a rule vanilla fails until checking which kind it is.

## The short version

Seven milestones, each ending at a check that can fail. M1-M3 are the engine and
are worth building even if the UI never happens, because the CLI alone answers
the question "is this set of tables any good". M4 is the UI. M5-M7 are the
generator, and they are the part most likely to be cut or deferred.

| | Milestone | Ships | Gate |
|---|---|---|---|
| M1 | Round-trip I/O ✔ | `model.py`, `cli.py` skeleton | 185 files load and save with a zero-byte diff — **passed** |
| M2 | Analysis engine ✔ | `analysis.py`, `cli report` | Monte-Carlo agreement on repel; survey numbers reproduced — **passed** |
| M3 | Linter ✔ | `lint.py`, `cli lint` | Vanilla passes the rules calibrated on vanilla — **passed** |
| M4 | UI ✔ | `server.py`, `ui/index.html` | Edit in the browser lands as the right one-key git diff — **passed** |
| M5 | Dupe-out planner ✔ | `planner.py`, `cli plan`, `/api/plan` | One hand-verified multi-step plan — **passed** |
| M6 | Generator, levels-only ✔ | `generate.py`, `cli generate` | A generated band clears R1/R2/R6 and reaches the R3 aim — **passed** |
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

**Accepted by Ian 2026-09-20.** The three bullets at the end of this section are
now house rules; M3 implements them rather than the design doc's R1 as written.

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

### M2 — Analysis engine — **done, 2026-09-20**

**Outcome first.** `PYTHONPATH=. python3 -m tools.oxide.encounters.test_m2` — 23/23.
The closed-form repel model agrees with a simulation of the game's own comparison
to within **2.62 sigma** across 292 comparisons, and vanilla reproduces the survey
on every headline number: 171 tables, median HHI **0.275**, p10-p90
**0.173-0.428**, spread **2.48x**, **71** distinct signatures, 5 species per table,
top slot 40%, rarest 5%, early **0.373** → late **0.275**, the ladder
`+0/+1/+1/+1/+2/+2/+2/+2/+2/+2/+3/+3`, and real tails on **6%** of tables.

**Two definitions the survey's prose left ambiguous, now pinned by measurement.**
The plan predicted this would be the risky part and it was.

- *Rarest-species uplift* has to break ties toward the best available uplift, not
  alphabetically. 29% of vanilla tables have several species at the minimum share.
  Tie-by-name gives 2.86x on 80% of tables; tie-toward-best gives **3.33x on 83%**,
  and that 83% is the survey's "rarest species survives the filter" column to the
  digit. R3's threshold of 3.0 is calibrated against this, so vanilla passes its
  own rule with room.
- *The survey's 5.0x* is not the rarest-species number at all. It is the best manip
  available to **any** species on the table, which measures **5.00x working on
  88%** — both exact. The column is headed "median uplift on rarest", so the
  heading is loose. Both statistics now ship: `uplift_on_rarest` and `best_uplift`.

**One survey number does not reproduce, and it matters.** Design doc 2.6 says only
**8%** of vanilla repel tiers collapse to a single species, and R6 is calibrated on
that. Measured on vanilla it is **24%** of rungs, with 43% of tables having at
least one singleton. No plausible variant of the definition gets near 8%.

What makes this more than a rounding dispute: the *base ROM's* tables measure
**7%**. That is suspiciously close to the doc's 8%, and the most likely explanation
is that this one figure was computed against `res/field/encounters/` in a working
tree that already held the base ROM's tables, rather than against vanilla. It is a
hypothesis, not a finding — but R6's threshold should be re-derived from vanilla's
24% before it is enforced, exactly as R1's was. Two rules calibrated against the
wrong thing is a pattern worth watching for in the rest of section 7.

"2x or better 69%" also fails to reproduce under any variant tried (the two
candidate readings give 66% and 81%). Both unreproduced numbers back *warn* rules,
and every rule that carries the design — R8 spread, R9 signatures, R11 arc — checks
out exactly.

**What the engine says about the tables the project currently has.** Running
`report` against the working tree instead of `main` is the first real payoff, and
it confirms two of Ian's three complaints as measured facts:

| | vanilla | current tables | target |
|---|---|---|---|
| HHI median | 0.275 | **0.185** | — |
| HHI spread (R8) | 2.48x | **2.14x** | ≥2.2 — **fails** |
| signatures/table (R9) | 0.42 | **0.26** | ≥0.35 — **fails** |
| species per table | 5 | **8** | 3-5 early |
| arc, early → late (R11) | 0.373 → 0.275 | **0.143 → 0.230** | decreasing — **fails, runs backwards** |
| real tails | 6% | **67%** | per archetype |
| binary manips | 24% of rungs | 7% | — |

Complaint 3 ("every route looked the same") is R8 and R9 failing. Complaint 2
("early didn't feel like early") is the arc running backwards — early tables are
*flatter* than late ones, the same inversion the survey found in Elite Redux and
Inclement Emerald.

Complaint 1 is the interesting one, because the numbers refute the obvious
explanation. The current tables' repel uplift is **6.67x working on 99%**, better
than vanilla's 5.00x on 88%. Manips are not weak here. What they are is *binary*:
67% of tables carry a genuinely exclusive 1-2% tail, so a repel resolves to one
guaranteed thing rather than to a smaller, richer pool. That is precisely what Ian
described as the failure — "a manip for something that is 'guaranteed' has very
binary logic" — and it means the fix for complaint 1 is not more uplift but fewer
exclusive tails and more re-weighting, which is what vanilla does and what the
archetype table's `duplicates` tail policy encodes.

### M2 — how it was built

`analysis.py`, pure functions, no I/O and no globals. Write it rate-array-agnostic
from the first line — take the rate tuple as an argument, defaulting to
`model.LAND_RATES` — so water and fishing tables are later a config change rather
than a rewrite. Then `cli report`, which is just a printer over it.

**The functions, and the exact semantics each has to honour.**

```
merged(table)            -> {species: share}   share = Σ rates of slots holding it
hhi(shares)              -> float              Σ share², shares summing to 1
rungs(table)             -> [level]            sorted distinct slot levels
pool(table, lead_level)  -> {species: share}   renormalised over surviving slots
conditional(pool, owned) -> {species: share}   drop owned, renormalise
throughput(pool, owned)  -> float              expected encounters per counting one
```

Three semantics to get right, all of them cheap to get wrong:

1. **A slot survives when `slot_level >= lead_level`.** Greater-or-*equal*. The game
   is `return repelActive && firstBattlerLevel > wildLevel`, so a level-14 lead
   still meets level-14 wilds. An off-by-one here silently changes every number the
   tool prints.
2. **A blocked roll cancels the step; it does not reroll.** So conditional on an
   encounter happening, the distribution is exactly the surviving slot weights
   renormalised. Nothing is smeared onto the survivors. This is why the model is
   exact rather than approximate, and it must never be "improved" into a reroll.
3. **Collapse rungs that yield the same pool.** Four distinct levels that produce
   three distinct pools are three rungs. Report three. The UI later shows rungs as
   *choices the player has*, and a rung that changes nothing is not a choice.

Shares are over merged species, not slots — a species in two slots is one entry at
the summed weight. HHI, signatures and "rarest species" all read from the merged
view.

**Then the metrics.** Per table: `n_species`, `top_share`, `min_share`, `hhi`,
`rung_count`, pool size per rung, `uplift_on_rarest`, `has_real_tail`, `band`.
Per game: HHI p10/median/p90 over tables with 3+ species and the p90/p10 ratio,
distinct weight signatures and signatures-per-table, early/mid/late medians, and
per-species area count and share range.

`uplift_on_rarest` is the headline number and the one the design turns on: take the
species with the smallest merged share, find the rung that maximises its share, and
divide by its base share. A table "has a working repel" when that ratio beats 1.

*Gate:* two checks, both from design doc section 11.

1. **`pool()` against a simulation.** Brute-force `RepelPreventsEncounter` over 10⁶
   trials on 20 random tables and compare to the closed form within Monte-Carlo
   error. The repel model is the tool's core claim, so it gets verified against the
   actual comparison rather than against a restatement of it. Seed the RNG so a
   failure is reproducible.
2. **`report --ref main` reproduces the survey.** On vanilla: median HHI **0.275**,
   p10-p90 **0.170-0.420**, **71** distinct signatures over 171 tables, median
   uplift **5.0x** with a working repel on **88%** of tables, median **5** species
   per table, top slot **40%**, and the slot-level ladder
   `+0/+1/+1/+1/+2/+2/+2/+2/+2/+2/+3/+3`. Early-to-late HHI should read
   **0.37 → 0.28**.

**A warning about that second gate.** The survey's own scripts (`unify.py`,
`repel.py`, `layout.py`) were written on the chat surface and are *not* in the repo,
so M2 re-derives these numbers rather than re-running them. The definitions above —
particularly "signature" and "uplift on rarest" — are read off the survey's prose
and are the least certain part of this milestone. If a number comes out close but
wrong, suspect the definition before suspecting the arithmetic. Write down whichever
definition reproduces the survey, because that is the one the linter's thresholds
were calibrated against.

A *signature* is the table's merged shares as a sorted descending tuple, e.g.
`(40,25,20,10,5)`. Vanilla having 71 distinct ones across 171 tables is the 0.42
figure in R9.

### M3 — Linter — **done, 2026-09-20**

**Outcome.** `PYTHONPATH=. python3 -m tools.oxide.encounters.test_m3` — 18/18.
Vanilla trips no errors and is silent on R8, R9, R11 and R14. The project's
current tables trip **R8 as an error** (spread 2.14x against the 2.2 floor) and
warn on R9 and R11. `lint --fail-on error` exits 0 on vanilla and 1 on the working
tree, so it is ready to wire as a pre-commit hook once the tables stabilise.

**The finding that shaped the milestone: the design doc mixes two kinds of
threshold and never says which is which.** R1 was the first case and Ian accepted
the fix; calibrating the rest surfaced three more. The distinction is now explicit
in `lint.py`:

- A **descriptive** threshold states something vanilla already does, so acceptance
  criterion 6 applies: if vanilla fails it, the threshold is wrong. R1b, R2, R6,
  R8, R9, R11, R14.
- An **aspirational** threshold is set beyond vanilla on purpose, because the
  design wants something the base game did not do. Vanilla is *expected* to fail
  these. R3, R5, R11b, R13.

Measured on vanilla, which is what sorted them:

| Rule | Vanilla | Verdict |
|---|---|---|
| R1b Spearman ≥ 0.5 | 71% of tables, corpus median 0.68 | descriptive, passes |
| R2 3-4 rungs | 81% | descriptive, passes |
| R6 ≤1 singleton rung | 84% | descriptive, passes |
| R8 spread ≥ 2.2 | 2.48 | descriptive, passes |
| R9 signatures/table ≥ 0.35 | 0.42 | descriptive, passes |
| R11 arc decreasing | 0.373 > 0.325 > 0.275 | descriptive, passes |
| R14 land_rate variety | 37% on the commonest value | descriptive, passes |
| R3 uplift ≥ 3.0 | **52%**, median 3.33 | aspirational |
| R5 band fit | **11-32%** | aspirational |
| R11b early ≥.35, late ≤.25 | early passes, **late is 0.275** | aspirational |
| R13 share span ≥ 4x | **37%**, median 2.5x | aspirational |

Two of these are worth Ian's attention because the design doc asserts them *as
descriptions of vanilla* and they are not:

- **R11's "late ≤ 0.25".** Doc table 2.1 records vanilla as 0.37 → 0.28 and then
  sets the target at ≤0.25, while criterion 6 says vanilla passes R11. It cannot.
  R11 is now split: the *shape* requirement (strictly decreasing) is descriptive
  and vanilla passes it; the absolute bounds became R11b, aspirational.
- **R13's 4x share span**, which the doc calls one of the three rules that carry
  the design, citing Starly at 20% on one route and 4% on another. Vanilla's median
  span is **2.5x** and only 37% of repeated species reach 4x. The rule is still a
  good idea — it is the one that makes Drayano-style availability generate variety
  — but it asks for roughly double what vanilla does, and that should be a choice
  rather than a surprise.

R6's threshold also needed re-deriving, as M2 flagged: the doc's "8% of repel tiers
collapse to a single species" is really 24% on vanilla. The *rule* as written (at
most one singleton rung per table) is fine and passes 84% of vanilla, so the rule
survived and only its stated justification was wrong.

**R12 reports itself as skipped** rather than silently passing, because the species
pick-list has no `tier` field yet. A rule that cannot run must say so — which is
also the lesson from a bug caught here: R11 was silently skipped on the first run
because bands arrived as `None`, and a quiet skip is indistinguishable from a pass
in the output. `lint_game` now emits a `skip` finding in that case and `test_m3`
asserts R11 actually evaluated.

Thresholds all live in `docs/oxide/encounters/design.json` and a test asserts that
editing one changes the verdict, so none can quietly drift back into code.

### M3 — how it was built

`lint.py` over M2's output, thresholds read from the sidecar, never hardcoded.
R1-R14 plus R1b. Severity as the design doc has it, with R1 scoped to authored
tables and R12 (availability) stubbed to a warning until the pick-list tiers exist.

*Gate:* `lint --ref main` passes R1b, R8, R9 and R11 on vanilla. If a rule vanilla
was derived from fails vanilla, the threshold is wrong — that is the whole point of
the check, and it has already caught R1 once.

### M4 — The UI — **done, 2026-09-20, pending Ian's usability pass**

```
PYTHONPATH=. python3 -m tools.oxide.encounters.server
# then open http://localhost:8765
```

`PYTHONPATH=. python3 -m tools.oxide.encounters.test_m4` — 41/41. The gate holds:
a slot edit made over the same HTTP the page uses lands in `git diff` as one line
at the right key, a day-layer write adds exactly one more, and a `land_rate` write
one more again. The test restores every file it touches, so it can be run against a
dirty tree without fear.

`server.py` is stdlib-only on `127.0.0.1:8765` and `ui/index.html` is one page of
vanilla JS with no build step and no CDN. Every number on screen comes from
`analysis.py` or `lint.py` through the API — there is no second implementation of
the maths in JavaScript, so the page and the CLI cannot drift apart.

**Layout.** Left is the area list with a lint dot, species count, HHI and uplift,
sortable by any of them; typing `/gible` filters to every table holding that
species, which is the question the dupe-out cascade is always asked in. Centre is
the twelve-slot editor with the merged view beneath it, and morning/day/night tabs
where day and night expose only slots 2 and 3 and grey the rest. Right is the live
analysis: the uplift number in green or red against R3, the ladder rung by rung,
a dupes checkbox per species that reweights every rung as you tick it, and this
table's lint findings with the aspirational ones marked. The header carries the
game-wide numbers — spread, signatures per table, the arc, lint totals — coloured
against their thresholds, so a local fix that drifts the global shape is visible
without leaving the table.

**Two things worth knowing.**

The species field is a `datalist`, which browsers treat as a suggestion rather than
a constraint, so a typo would otherwise write a species that does not exist and
break the next build. The server validates every write against the 496 constants
derived from `res/pokemon/` and refuses anything else with a message the page
shows; levels outside 1-100 and slots outside 0-11 are refused the same way, and a
refused write changes nothing on disk. `include/generated/species.h` is a build
artefact and absent from a clean tree, which is why the universe comes from the
directory listing — all 329 species used across the encounter files are covered.

Edits write on blur and save immediately; there is no save button to forget. If a
write is refused the field is reloaded from disk rather than left showing something
that was never stored.

**Revised after Ian's first usability pass, same day.** Five changes:

- **Names are names.** `SPECIES_GLALIE` is shown as *Glalie* everywhere — list,
  editor, merged view, ladder. Six constants plus `farfetchd` need special casing
  (`Nidoran♀`, `Nidoran♂`, `Mr. Mime`, `Mime Jr.`, `Ho-Oh`, `Porygon-Z`,
  `Farfetch'd`); the rest title-case. The mapping lives server-side so the page
  never has to know about constants, and every payload carries a `label`.
- **Play order is the default sort**, approximated by encounter level until a real
  progression order exists in the sidecar. It reads Route 201 → 202 → Lake Verity
  → 204 South → 203 → Ravaged Path → Oreburgh Gate and ends at Stark Mountain,
  which is close enough to Sinnoh's actual route that the approximation is
  carrying its weight. Replacing it with the explicit order M5 needs is a one-line
  change to the sort key.
- **Every species cell is a combobox** over the whole 496-entry dex: type to
  filter, or click the caret to browse. Arrow keys move, Enter picks, Escape
  reverts. It replaces the `datalist`, which browsers render inconsistently and
  which gave no way to *browse* rather than recall.
- **The area filter is frozen** at the top of the left column, so it stays usable
  however far the list is scrolled.
- **A caught column**, and it is global. Ticking a species in one table removes it
  from the counting mass in *every* table, because that is exactly what the dupes
  clause does — the reason a distant table is worth walking to is what it lets you
  delete from a later one. Ticking Bidoof moves six tables and lifts Route 201's
  odds on its rarest from 2.0% to 2.7%. The left list then shows how many species
  a table still owes you and the best reachable odds on the rarest of them, and a
  fully-caught table greys out.

Caught state is per-playthrough, not design intent, so it lives in
`docs/oxide/encounters/caught.json` and is gitignored. It is held server-side
rather than in the browser so that it is genuinely one list: every table's numbers
are computed against it, and reopening the page does not lose it.

**Second round, same day.** Four more changes, two of which reach into the model.

- **The dupes clause now works on evolution lines, not species.** Catching Starly
  on Route 201 zeroes Staravia on Route 205 North too, because that is how the
  clause is actually played. Families are the connected components of the
  evolution graph read from each species' `data.json`, in a new `dex.py` that also
  owns the display names. One bug caught on the way: evolution entries vary in
  arity (`["EVO_LEVEL_MOSS_ROCK", "SPECIES_LEAFEON"]` puts the target at index 1,
  `["EVO_USE_ITEM", "ITEM_THUNDERSTONE", "SPECIES_JOLTEON"]` at index 2), and an
  index-2 assumption silently dropped four of Eevee's seven. The target is now
  found by scanning for the `SPECIES_` element. A species duped out by a relative
  shows a *line caught* tag and a disabled checkbox rather than a tick.
- **The centre column shows real odds.** Both the slot table and the merged view
  carry a "real odds" column beside the on-paper rate: a caught or duped species
  reads 0% and is struck through, and everything else renormalises so the column
  still sums to 100%. Route 202 after catching Starly: the two 20% slots read
  21.1%, the 10% slots 10.5%, and Starly 0%.
- **The area list fades with progress** rather than flipping at "all caught":
  four steps of opacity from untouched to done, with the name struck through only
  when nothing is left. The "left to catch" count spans every table kind an area
  has, so a route whose only outstanding species is in its surf table does not
  read as finished.
- **Surf and the three rods are in.** They were out of the first pass by the
  design doc's own scope, but the data was always in the same files and the
  analysis layer was built rate-array-agnostic for exactly this. Fifty-three
  areas have water tables. The slot rates come from `GetWaterEncounterSlot` and
  `GetRodEncounterSlot`: surf and old rod `60/30/5/4/1`, good and super rod
  `40/40/15/4/1`. Water slots carry a level *range*, and `GetWildMonLevel` rolls
  uniformly inside it, so a repel there admits a **fraction** of a slot rather than
  all or nothing. The repel model was generalised to (species, lo, hi) with land
  as the degenerate lo == hi case — M2's 23 checks still pass byte-identically,
  which is the proof the generalisation cost land nothing. On Route 205 South's
  surf table, a level-30 lead drops Grimer from 60% to 40.6% because only one of
  its eleven levels survives, while Tentacool's wider range keeps most of its
  mass. That is a real manip surface the land-only model could not see. Lint
  stays land-only, since every rule was calibrated on land.

**The design pass.** Reviewed against the frontend-design skill's list of
generated-page tells, the first version hit three of them: a near-black ground
with one acid accent (it was, in fact, the Tokyo Night palette), tracked-out
all-caps eyebrow labels, and meta strings joined with middle dots — which was also
the thing hardest to scan. The rewrite is a cold pale instrument rather than a
dark dashboard: one mineral teal reserved for probability mass, one warm ochre
reserved for the single number worth acting on (the uplift), deep red only for
lint errors, and anything already caught drawn as *absence* — hatched, hollow,
struck — rather than in another colour. Prose is in the system sans in sentence
case; monospace with tabular figures is used only where numbers must align down a
column. The one bold element is the repel ladder, now drawn as proportional bars
per rung with caught species hatched, so the mass visibly moves to the survivors
when a box is ticked.

**Third round, same day: caught state is per area.** Ian asked for a column
saying *what was caught there* and an "Encounter:" heading on the centre table.
Both imply the nuzlocke model the dupes clause comes from — one encounter per
area — so the caught record changed shape from a bare species list to
`{area: species}`. Ticking a species records it against the area being edited;
ticking a second species on the same area replaces the first; unticking clears
that area. A species duped out by a relative now says where and by what
("Starly, route 201") instead of a bare *line caught* tag, and the whole-dex
owned set is still derived by expanding every recorded encounter's line. The
area list gained the encounter column, the centre header carries the encounter in
large type at top right, the species cell was cut to 11.5em from filling the
column, and the centre's type went up to 15.5px. 46/46.

This is also where the tool's footprint in `tracker.md` was formally cut to one
paragraph by the other track's docs pass ("one home per fact"); per-milestone
records live here from now on, which is what has been causing the merge
conflicts to stop.

`server.py` on `127.0.0.1:8765`, stdlib only, and `ui/index.html`, vanilla JS, no
build step and no CDN. Three columns as specified: area list with sortable HHI,
twelve-slot editor with merged and ladder views, live analysis panel with the
dupes checkboxes. Write on blur.

Build it against M2's JSON and nothing else — every number on screen is an
`analysis.py` call, so there is no second implementation of the math to drift.

*Gate:* edit a slot in the browser, see it in `git diff` at the right key with no
other key touched.

### M5 — Dupe-out planner — **done, 2026-09-20**

**Outcome.** `PYTHONPATH=. python3 -m tools.oxide.encounters.test_m5` — 13/13,
first run. The gate is the design doc's own thought experiment built as two
synthetic tables small enough to do by hand: 98% Rattata in front of 2% Mewtwo,
with Rattata catchable one route earlier. Unplanned, Mewtwo is 2% and the first
counting encounter costs one battle. Catch Rattata first (1/0.98 = 1.0204
encounters at its best rung), and Mewtwo becomes the only thing that counts: 100%,
for 1/0.02 = 50 battles at the target, 51.0204 in all. The planner returns exactly
those two Pareto points, to nine decimals.

On a real table it does what the doc promised. Route 214's Growlithe sits at 1% on
paper and 3% behind a level-29 repel. The planner finds the cascade: catch Gulpin
first (Great Marsh, **old rod**, 52%), then Rhyhorn (Ravaged Path, 50%), Meditite
(Wayward Cave, 22%), Girafarig (Route 206, 20%) and Doduo (Route 201, 8%) — five
earlier routes, one catch each — and Growlithe is the *only* thing that counts on
214: **3% → 100%**, about 61 encounters in all. The front has eleven points between
those two, each buying more odds for more cost, and the page shows them as
sentences. `cli plan encounters_route_214 growlithe` prints the same.

**Two things the per-area caught model changed about the doc's description**, both
enforced and both tested:

- **A source consumes its area's one encounter.** Sources must be earlier in
  progression than the target, must have no encounter recorded yet, and each
  supplies exactly one line. The doc's own example — "pre-catch Hippopotas on Route
  214 itself" — is not legal under this rule and the planner will not propose it.
- **Removal is by line**, so any member of a family caught anywhere earlier
  removes the whole family from the target, and the search enumerates subsets of
  *lines* on the target table, not species.

**One modelling choice to know about.** Acquisition cost is the doc's "expected
encounters until it appears", 1/P at the best rung of the best source, which
assumes the player can flee a non-target and keep going. The one-shot odds — the
chance the very first counting encounter at the source is the target — are
carried in every acquisition beside it, so if Ian plays strict one-encounter, the
number he needs is already there; switching the optimisation to it is a one-line
change.

Progression order is still approximated by encounter level, the same key the page
sorts by. The planner reads it from one place (`plan_inputs`), so the sidecar's
real order drops in there when it exists. Water tables are already sources: the
Gulpin above comes from a rod.

*Gate was:* one hand-verified case, worked out on paper first and then matched.

### M6 — Generator, levels-only — **done, 2026-09-20**

```
PYTHONPATH=. python3 -m tools.oxide.encounters.cli generate --band early --dry-run
PYTHONPATH=. python3 -m tools.oxide.encounters.cli generate --area encounters_route_201 --aim 10
```

**Outcome.** `PYTHONPATH=. python3 -m tools.oxide.encounters.test_m6` — 19/19. This
is step 3 of design section 8.2 shipped alone, as the plan advised: species stay
where Ian put them and the generator chooses each slot's level so the repel ladder
under them pays. Full species placement (steps 1, 2 and 4) is deferred and may
never be needed.

**Not a hill-climb.** The house rule R1 — levels non-decreasing with slot index —
makes the search tiny: a twelve-slot ladder over four rungs is a choice of where
three steps fall, **455 ladders**. So the generator enumerates every one and picks
the best exactly. The paper case is a four-species route shape whose optimum can
be worked out by hand (the rarest species isolated on the top rung with its
lightest companion: 60%, a 10x uplift); the search finds it.

**The objective, and why it changed.** The first version maximised uplift on the
rarest species outright, and it turned every early table into the same thing —
the 1% species isolated with its lightest companion at 50%, a **50x uplift on all
sixteen** — which is exactly the homogenisation the design exists to prevent. So
the objective *satisfices*: every hard rule first (R1 by construction, R2 rung
count, R6 singleton and top-rung width), then the smallest shortfall below an
**aim** (R3's threshold, 3.0x, by default), then the fewest slots changed, then
the widest top rung, and only then the highest uplift. At the default aim the
early band lands at 5x to 50x across five distinct values with top rungs of two
to four species; `--aim 100` still reaches the 50x band, deliberately available,
deliberately not default.

**One consequence Ian should know before running it for real.** The search only
ever yields ladders that obey R1, and **88% of the tables on this branch do not**
(M1's finding). So the generator changes something on almost every table, and a
table whose illegal ladder happened to pay well can come out paying less: Valley
Windworks Outside and Oreburgh Gate 1F both go from 20x to 16.7x. That is the
house rule doing its job, not a defect, and the CLI says so in its summary line
when it happens. If Ian would rather keep a non-monotonic ladder that pays, R1 is
his to relax.

Locked slots (`locked` in the sidecar) keep their level. Writes go one key per
changed slot through `model.set_slot`, so a run is a readable git diff; there is no
separate repairs log because the diff is the record. Nothing is written without
dropping `--dry-run`.

One unreproduced oddity, recorded so nobody chases a ghost: a single run of the
gate, immediately after two files were patched, died with a `TypeError` inside
`analysis.best_uplift` on the `--aim 100` path. Four full reruns since, including
the exact same sequence with the function instrumented, all pass 19/19, and a
scan of every ladder on every early table scores cleanly.

*Gate was:* `generate --band early` produces tables that clear lint without hand
repair. Read against levels-only: every proposal clears R1, R2 and R6 and reaches
the R3 aim, with nothing written.

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

1. ~~**R1's demotion.**~~ **Answered 2026-09-20: accepted as proposed.** R1 stays an
   error for Oxide-authored tables, R1b (warn, Spearman ≥ 0.5) is the calibration
   form, and acceptance criterion 6 drops R1 from the list of rules vanilla must
   pass. M3 implements this; no further confirmation needed.
2. **Progression order.** M5 needs an explicit area order and the sidecar does not
   have one. Is there an existing ordering to reuse, or does it get hand-written
   once into `design.json`?
3. **Species tiers.** R12's availability thresholds need the pick-list's `tier`
   field populated (`starter-adjacent` / `preferred` / `filler` / `gate`). Until
   then R12 stays a warning. This is Ian-only work and gates M3's last rule.
4. **Scope of the first authored pass.** 171 land tables is a lot of hand design.
   Is the target all of them, or a corridor — say the first third of the game — to
   prove the model before committing?

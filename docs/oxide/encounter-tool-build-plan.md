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
else. Its footprint in `tracker.md` is one paragraph (design doc rule 11).

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
PYTHONPATH=. python3 -m tools.oxide.encounters.test_m8     # expect 60/60, the dex and moves
PYTHONPATH=. python3 -m tools.oxide.encounters.cli generate --band early --dry-run
python3 tools/oxide/verify_narcs.py --built build/pokeplatinum.us.nds --source   # M7, after make rom
PYTHONPATH=. python3 -m tools.oxide.encounters.server      # the UI, localhost:8765 (--port for a second checkout)
```

The `--source` line is the one that closes the loop: it needs a built ROM and no
reference ROM, and it must read "all 183 tables match their source JSON". It is the
only check here that looks at what the game actually runs.

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

**The tool is complete: all seven milestones are done.** Their sections below
record what each found; M6 shipped in its levels-only form, and full species
placement is deferred, possibly for good. **Next is the authoring pass**, which a
separate agent picks up: Ian called M4 done for now on 2026-09-20 and asked for the
tables themselves to be written from the pick-list. The plan for that is
`docs/oxide/encounter-authoring-plan.md`: read it next, it says what to do in what
order and which decisions are already taken. Its Step 0 adds the small pieces of
tooling the pass needs (`cli apply`, `cli audit`, `cli coverage`, writers for the
remaining encounter keys); the source-versus-ROM check it also lists is M7, which
is now built and is the gate every authored batch must clear before it is called
done. Step 1 supplies the progression order and tiers. Status for the pass goes in
an "Authoring pass" section below, gate by gate. This chat keeps the tool's design
and any additions to it; the pass is someone else's.

**Before running the generator for real, read M6's "one consequence"**: it enforces
R1, most current tables break R1, so it will change almost every table it is
pointed at and a few will pay less than they did. Use `--dry-run` first.

**Three decisions already taken**, so they do not need rediscovering. Writes go
through `jsonstyle.replace_value` on file text and never re-serialise a whole file.
The design doc's R1 is amended as its section 7 records (v1.1), accepted by
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
| M7 | ROM verification ✔ | `verify_narcs.py --source` | Built ROM's NARC matches the source JSON — **passed, 183/183, 21,045 fields** |

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

### M7 — ROM verification — **done, 2026-09-20**

```
make rom
python3 tools/oxide/verify_narcs.py --built build/pokeplatinum.us.nds --source
```

**Outcome.** `verify_narcs.py --source` compares `pl_enc_data.narc` in a built ROM
against `res/field/encounters/*.json` field by field, with no reference ROM
involved. Run against the current build: **all 183 tables match, 21,045 fields
checked, nothing skipped.** That build came from the main checkout, whose 188
encounter files are byte for byte identical to this branch's, so it was a valid
build of the current data and the first run needed no rebuild.

**Why it is its own mode rather than a flag on `--encounters`.** The existing
check proves a build matches the *base ROM*, and deliberately skips the six fields
the importer left at vanilla (`unown_table`, `rate_form0..4`). That reference stops
being the truth the moment a table is authored, and the skips would then hide real
drift. `--source` proves the build matches the *JSON*, the only thing that stays
authoritative, and skips nothing: the JSON is what the build wrote from, so every
packed field must round-trip, those six included. Per design doc 8.4, the
generator reports success from lint, lint reports from disk, and this reports from
the thing the game actually runs.

**Three things the run settled.** The decoder is the converter run backwards and
yields species by *name*, so a decoded record compares directly against the JSON
on the keys the packed record carries. It resolves those names through
`generated/species.txt` when there is no build directory, so the check runs from
a clean tree. And the three JSON keys it reports as not compared —
`map_category`, `elusive_rod_encounter`, `daily_encounters` — are keys the
converter never packs, confirmed by reading `tools/jsoncnv/encounter.py`, so
"nothing skipped" is a claim about the whole 424-byte record. The NARC holds
exactly the 183 land tables in `encounters.order`; the two non-land files are
built separately through `encdata_ex.order` and are not members.

`--ref` is no longer required by the argument parser — every check except
`--source` asks for it explicitly — and the old `--encounters` mode still passes
on the same build.

**For the authoring pass:** this is the gate each authored batch clears. Build,
then `--source`; it must read "all 183 tables match their source JSON". A table
that lints clean but fails here has been written to the JSON in a way the
converter does not carry, and that is a bug in the writer, not the table.

*Gate was:* `make rom` after a generated pass, then a clean field-by-field
compare.

## Authoring pass

Status for `docs/oxide/encounter-authoring-plan.md`, gate by gate. The plan
says what each step is; this says what happened.

### Step 0 — tooling — **done, 2026-09-20**

```
PYTHONPATH=. python3 -m tools.oxide.encounters.test_step0        # expect 35/35
PYTHONPATH=. python3 -m tools.oxide.encounters.cli audit --summary
PYTHONPATH=. python3 -m tools.oxide.encounters.cli coverage
PYTHONPATH=. python3 -m tools.oxide.encounters.cli apply AREA --dry-run
```

**What was built.** In `tools/oxide/encounters/`: `model.py` gained
`set_swarm`, `set_radar` and `set_dual_slot` (the same `_replace` path as
`set_time_slot`, one key per write) and species-only readers for the honey
tree, the Great Marsh lookout and the Trophy Garden dailies, plus
`Area.reference_species()` for the audit; `dex.py` gained `constant_of` (the
reverse of `display_name`, so the pick-list's "Nidoran F" and "Mr. Mime"
resolve), `pick_list` and `line_base`; `audit.py` is new and holds the leak
audit and the availability coverage; `layout.py` is new and holds the slot
layout behind `cli apply`; `cli.py` gained `audit`, `coverage` and `apply`.
Outside the tool: `import_base_rom.py` has an `AUTHORED` table mirroring
`bulk_scripts.py`'s `DIVERGED`, and `authored_encounters()` unions it with
every sidecar area that has a `cast`, so a table authored through `apply` is
protected from the importer without a second list to maintain; the dry run
reports those as "authored, skipped" and counts 0. `verify_narcs.py
--encounters --ref` skips the same set and names them (`--source`, M7, is
their check). `integrate.sh` now runs `--encounters --source` and every
`test_*.py` in the tool directory.

**The M7 item on the plan's Step 0 list was already done** by the tool track
the same day (`verify_narcs.py --source`, section M7 above), so it was not
built again; the plan predates M5 to M7.

**The layout rule, as implemented.** The archetype's signature is the merged
shares in cast order. The twelve slots are walked in index order and each is
given to a species whose remaining share covers its rate, backtracking when a
partial layout cannot complete, so every species' slots sum to exactly its
share and the first-listed species is the 20% face. Levels are `base_level`
plus a per-slot offset from the entry's `ladder` or the archetype's default
(four rungs: vanilla's `0/1/1/1/2/2/2/2/2/2/3/3`; three: `0/0/1/1/1/1/2/...`;
two: six and six; one: flat), so R1 holds by construction. A cast entry
`{"species": X, "rung": r}` guarantees X one slot on rung r. One finding
worth knowing before authoring: **tight signatures decompose only one way.**
A5's 40 can only be the two 20% slots and its 1s the two 1% slots, so an A5
head can never sit on the top rung, whatever the ladder; A1's 10 and 5 leave
room (5+4+1, 4+1), which is where the "duplicate of a head species on the top
rung" of the authoring rules comes from. `apply` refuses a pin the arithmetic
cannot honour and says so. It also refuses to change a `locked` slot; a lock
should be expressed as a pin. Levels come out as the plain ladder; M6's
`generate --dry-run` can then tune them for R3 if the table needs it.

**Gate, on the unchanged tree.** M1 13/13, M2 23/23, M3 18/18, M4 46/46, M5
15/15, M6 19/19, Step 0 35/35; `lint --ref main` 0 errors, `lint` 1 error
(R8), both as before. `verify_narcs --encounters --source` against the main
checkout's build: 183 of 183 tables, 21,045 fields. `import_base_rom.py
--dry-run --skip-text`: every count 0, "0 authored table(s) left alone".

The audit's numbers, and how they sit against the plan's "facts that size
it": live land slots **2,052 with 1,250 off-list** (exact match); water and
rods **641** off-list references ("about 640"); **183 of the 183 land-format
files** reference an off-list species somewhere, and so do both non-land
files. Over every key in every file, **404 distinct species are referenced,
259 off-list**; over live land tables alone it is 302 and 189. The plan's
375 / 237 pair is reproduced to within one or two by "live tables, land +
water + radar + dual-slot" (374 / 236), so it was a different key selection,
not a different tree; the audit prints the per-key table rather than
choosing one. Natives in no live land table: **86**; in no encounter source
of any kind: 54; the plan's 61 is the land + water + dual-slot count. Radar
488, swarms 250, day/night 440, dual-slot 1,092 off-list references. Scripts:
88 give or battle commands name a species, **43 off-list**, listed in the
audit output for Ian (decision 8): the base ROM's house gifts in Sandgem,
Floaroma, Solaceon, Pastoria, Veilstone and the Canalave library, the Day
Care Ditto, and the Twinleaf legendary battles (Mewtwo, Mew, the beasts,
Lugia, Ho-Oh, Celebi, the weather trio, Jirachi, Deoxys).

Coverage on the unchanged tree, by evolution line: **99 native lines**: 35
with a wild home, 38 with a non-wild source only (gift, trade, static battle,
starter or fossil), 12 water-only, 8 cameo-only, 1 other-only (Yanma: marsh
binoculars and dual-slot), and **5 with nothing**: Articuno, Zapdos, Moltres,
Mesprit and Cresselia, which Platinum places as roamers through a mechanism
no script names. The 159 new species are listed separately as not in the
tree. R12 stays skipped until Step 1 writes `tier`.

*Gate was:* M1 to M4 tests pass; `integrate.sh --dry-run` passes; audit and
coverage run on the unchanged tree with numbers matching the plan's facts.

### Step 1 — order and tiers — **done, 2026-09-20**

```
PYTHONPATH=. python3 -m tools.oxide.encounters.test_step1        # expect 21/21
PYTHONPATH=. python3 -m tools.oxide.encounters.cli lint --rule R12 --all
PYTHONPATH=. python3 -m tools.oxide.encounters.cli --ref main lint --rule R12 --all
```

**What was written.** Every one of the 185 sidecar areas carries `order`,
1 to 185, from the plan's outline expanded to file names in
`progression.py` and written once by `cli order-init` (the twelve
`land_rate` 0 files and the two species-only files got minimal entries so
they carry a position too). The pick-list has a `tier` column on all 360
rows, derived once by `cli tier-init` from `tiers.py` and appended without
touching any other byte of the CSV: gate 102, starter-adjacent 16,
preferred 83, filler 159. Both writers refuse to run twice without
`--force`, so Ian's corrections in the sidecar and the CSV are safe from a
re-run. The planner's play order now reads the sidecar's `order` instead
of approximating it by level (the one-line change the M5 notes promised).

**Placements the outline did not settle**, for Ian's correction: the Old
Chateau sits after Eterna Forest; Route 207's single file at its first
mention (before Oreburgh Mine); Mt Coronet's north room 1 (level 13-16)
with Route 211 west and the rest of the mountain in one climb after Lake
Acuity; the Ruin Maniac's cave with Maniac Tunnel; Route 224 after
Victory Road's post-game rooms; Snowpoint Temple after the League; the
twenty-five `unknown_533` to `unknown_557` files (level 45-48, five
species, following Turnback Cave in the NARC) last, as the plan's
"post-game lake rooms".

**How the tiers were derived.** `gate` is legendaries and mythicals,
starter lines and fossil lines by national number, plus any species a
static battle command names. `starter-adjacent` is any native line whose
first stage vanilla places in an early-band land table (median level 12 or
under). `preferred` is Platinum's 210-species Sinnoh dex, read from the
pinned vanilla ROM's `pl_pokezukan.narc` (the repo's prebuilt
`pokezukan.narc` is Diamond and Pearl's 151). `filler` is the rest. A native
line takes one tier across its stages, the strongest member's. Twenty-one
native rows have no `natdex` in the CSV (their stats were UNMATCHED against
the spreadsheet), so the number comes from the tree's species order for
those; without that the three birds and Cresselia had landed in filler.
House gifts (Cherubi, Murkrow and the rest of the base ROM's additions) are
*not* gate: they are Ian's, and the plan's "anything scripted" was read as
the static battles.

**R12, as it now runs.** `audit.availability()` gives the linter one row
per native line: its tier, whether a script hands it over (gift, trade,
static battle, starter, fossil), and its cheapest wild acquisition, the
expected encounters to the first one at the best table and repel rung over
every live land and water table, with nothing owned. A gate line passes on
a scripted source and fails without one; any other line passes on a
scripted source or on a cost under its tier's ceiling. The ceilings are
`r12_max_cost` in the sidecar's thresholds, proposed at 5 / 20 / 100
encounters for starter-adjacent / preferred / filler, Ian's to move. Costs
count land and water only, not swarms, radar, the dual-slot lists, honey
trees or the marsh binoculars, since the design scoped the first pass to
land; a line vanilla supplies only through those (Heracross, Larvitar,
Beldum, Feebas) fails on `--ref main`, which is a true statement about
where the pass has to put them, not a bug. Without a `tier` column the rule
still reports itself skipped.

**Gate.** Step 1 21/21, Step 0 35/35, M3 to M6 still green. `lint` on the
working tree: 10 errors, 0 skipped, the R8 spread as before plus **9 R12
errors**: Articuno, Zapdos, Moltres, Mesprit, Cresselia and Phione as gate
lines no script names (the roamers and Manaphy's egg), and Yanma, Houndour,
Hippopotas as preferred lines with no wild table. `lint --ref main`: 22 R12
errors, R12 evaluated rather than skipped, as the plan asked. Because
vanilla was never built for the pick-list, `integrate.sh`'s vanilla lint
check now passes `--ignore R12` (a new lint option) and stays at 0 errors;
R12 is enforced on the working tree, where it belongs.

**Follow-up, 2026-09-21, after element 3.** With the 159 new species in the
tree the dex knows their lines, and five of them are new evolutions of native
lines (Kleavor, Gyarados M, Sylveon, Clodsire, Lopunny M) that had been tiered
by dex number alone. `tier-init --force` was re-run before Ian had touched the
CSV; exactly those five rows changed, to their line's tier, and the counts are
now gate 102, starter-adjacent 17, preferred 87, filler 154. Coverage runs over
**177 lines**, all resolvable: home 35, non-wild 38, water-only 12, cameo-only
8, other-only 1, and **83 with nothing**: the 5 roamers plus 78 new lines no
table or script names yet. R12 on the working tree: **87 errors**, the 9 above
plus those 78. That is the size of Step 2.

*Gate was:* R12 runs; `order` covers all 185 areas with no duplicates.

### Step 2 — the availability plan — **done, 2026-09-21**

```
PYTHONPATH=. python3 -m tools.oxide.encounters.test_step2          # expect 17/17
PYTHONPATH=. python3 -m tools.oxide.encounters.cli availability     # the gate
PYTHONPATH=. python3 -m tools.oxide.encounters.cli availability --write   # regenerate the doc
```

**What was written.** `docs/oxide/encounters/availability-plan.json` is the
design: for every live land table, the lines at home on it and the lines
that merely appear, by first-stage constant, with a one-line note per table;
plus the water tables that are the water lines' homes and a proposal per
gate line no script names. It is keyed by area on purpose, so Step 3 reads
a table's intended cast straight off it. `availability.py` turns it around
into the per-line view the plan asked for, joins it with the sources the
tree already has (gifts, trades, static battles, the starter, the fossils),
checks the gate and renders `docs/oxide/encounters/availability.md`, which
is generated and never edited; `test_step2` fails if the committed document
is not what the plan renders. `cli availability` is the gate, exit 1 on a
failure.

**The plan's shape.** 177 lines: **87 with a wild home, 53 scripted, 7 on a
water table, 30 proposed**, none without a source. Every line has exactly
one home; cameos number one to six per line and are where R13's variety and
the dupe-out structure will come from. Themes follow vanilla where the
pick-list allows (Shinx on 202, Gible under Wayward Cave, Wooper in the
marsh, Snover on 216, the Old Chateau as an A2 monoculture of Sinistea) and
the new species fill what the list dropped (Wooloo and Pikipek as the first
route's pair, Nacli for Geodude, Mienfoo for Meditite, Yamask in the Lost
Tower, Galarian Mr. Mime on 218 where Mr. Mime was). Multi-room areas share
a cast and vary it room by room. The twenty-five `unknown_533` to
`unknown_557` files turned out to carry Turnback Cave's deep cast at level
45, so they are its post-game rooms, planned as such, and the plan proposes
the Ultra Beasts as their static occupants.

**Two decisions taken to make the corridor possible.** Vanilla's early band
gives the pick-list only seven starter-adjacent lines, which cannot fill
seventeen corridor tables at three to five species. `tiers.py` gained
`EARLY_LINES`, the other regions' first-route lines, native and new
(Sentret, the Nidorans, Vulpix, Shroomish, Lotad; Purrloin, Sewaddle,
Minccino, Fletchling, Pikipek, Grubbin, Bounsweet, Rookidee, Blipbug,
Wooloo, Pawmi, Smoliv, Nacli), and `tier-init --force` was re-run before
Ian had edited the CSV: tiers are now **gate 102, starter-adjacent 68,
preferred 87, filler 103**. And the roamers (Articuno, Zapdos, Moltres,
Mesprit, Cresselia) and Phione, which no script names, are recorded in
`audit.SCRIPTED` as sourced by their vanilla mechanism, so they pass R12
instead of failing it as the Step 1 entry above reported.

**The gate, as the tool checks it.** No line without a home, a scripted
source or a proposal; the corridor (through Eterna Forest, 17 live tables)
carries only starter-adjacent lines and lines with a scripted source; every
starter-adjacent line's home is in the corridor; every early-band table has
two to five lines planned (two only for an A4 duo, Ravaged Path); every live
table has something planned. All pass. `lint` on the unchanged tables now
reads 81 R12 errors, the 30 new gate lines plus 51 wild lines the current
tables do not deliver under the ceilings; that is Steps 3 and 4's work.

**For Ian**, all in the document's own section and none blocking: the 30
proposals (the new starters as pick-one gifts in Eterna, Pastoria and
Snowpoint; the Galarian birds as roamers or statics; Xerneas and Yveltal at
Sendoff Spring and Route 224; the Tapus at the four shrines; the Ultra
Beasts in Turnback's post-game rooms; Diancie in Wayward Cave; Blacephalon
after Heatran; Poipole and Magearna as gifts); the widened starter-adjacent
tier; the water homes, which Step 5 only de-leaks unless surf is designed;
and one data gap, Fomantis and Lurantis being two lines in the tree because
Fomantis's data lacks the evolution, so each has a home of its own until
that is fixed.

**Revised the same day, on Ian's review of the proposals.** Three rules
from him, all now in the plan file and the document. Everything except the
two box legendaries must be possible before the first League clear, which
rules out the Battle Zone, Stark Mountain, Snowpoint Temple, Route 224,
Sendoff Spring and Turnback Cave (all National Dex in Platinum). Fewer
gifts, so the eight new starter lines are **wild and out of the gate tier**
(`WILD_STARTERS` in `tiers.py`): Fennekin on Route 214, Scorbunny on Route
206 and Popplio in the surf on Routes 219 and 220 at a real share, since he
wants those three to be a good chance with or without a manip; Litten
(Fuego Ironworks) and Froakie (Route 212 south) as tails a dupe-out plan
pays off; Rowlet, Snivy and Sprigatito in the honey trees' rare tier, which
makes the honey trees designed space from Step 5 on. And vanilla's three
pre-League legendaries already felt like a lot, so the twenty new ones are
**not statics of their own**: the two lake caverns become two static
battles drawn without replacement from one pool, and Mesprit's roamer a
random roamer from the same pool (Uxie, Azelf, Mesprit, the Galarian
birds, Zygarde, Diancie, the Tapus, the eleven Ultra Beasts, Magearna: 23
candidates, one list he can split). That scripting is outside this track;
R12 in the linter reads the tree and reports those lines until it exists.
Xerneas (Sendoff Spring) and Yveltal (Route 224) stay as the only new
statics, post-League by rule.

The tool learned two things for this: a honey-tree placement counts as a
source for R12 (the cost model cannot price a slathered tree), and the
document carries `honey` and `pool` statuses. The plan now reads **89 with
a wild home, 53 scripted, 8 on water, 3 in the honey trees, 20 in the pool,
2 proposed, 2 deliberate tails** (Litten, Froakie); tiers gate 78,
starter-adjacent 68, preferred 111, filler 103; Step 2 18/18; R12 on the
unchanged tables still 81 errors.

*Gate was:* no line without a source; the early band's cast fits 3-5
species per table with the lines whose tier says early.

### Step 3 — the first two splits — **regenerated twice on Ian's review, 2026-09-21; merged into `oxide` 2026-09-21**

```
PYTHONPATH=. python3 -m tools.oxide.encounters.test_step3                    # expect 28/28
PYTHONPATH=. python3 -m tools.oxide.encounters.cli apply --all --dry-run     # 24 areas, 0 failed, nothing to change
PYTHONPATH=. python3 -m tools.oxide.encounters.cli availability              # the gate, now with splits and caps
PYTHONPATH=. python3 -m tools.oxide.encounters.server                        # Ian's view: location and split on every row
```

**What Ian said, on the first seventeen tables.** Captures are per location
*name* (Lake Verity and its drained version, Route 204's halves, the gate's
floors: one capture each); the game is played in gym splits, each with a
hard level cap (Gardenia's is 26), and the rods arrive by split (Old Rod in
Roark's, Good in Maylene's, Super in Candice's), so a fishing spot is an
early capture wherever its water is; repel manips do not work on fishing or
honey trees; there is one Repel before Roark, so the early game is where
randomness is cheapest and a 50% face is monotony; no species over about a
third of a table, anywhere, as a soft rule; a location whose halves fall in
different splits is a delay and must be worth delaying for; the early caves
were thin, so Nosepass, Geodude, Phanpy and Makuhita join the early lines;
starter lines as 4%/1% one-off tails without lowering their rates elsewhere
is a move he likes; a line fully evolved by level-up under a split's cap
belongs in or before that split; the starter gets its own met location, so
Route 201 counts as a capture; and the clown gifts (Sandgem, Jubilife,
Oreburgh, Floaroma, Eterna) are levers whose species can change. When a
table cannot be filled from the list, stop and propose additions before
pushing.

**What was built.** `locations.py` reads the map headers and the location
names bank, so every table knows its capture area (63 named locations; the
Turnback rooms and the twenty-five unknown files have no header). The
sidecar carries a `split` per area and a `splits` table (order, caps, rods;
`cli split-init`, once), with `water_split` for Route 218, whose fishing
spot is a step from Jubilife while its grass is by Canalave. Two archetypes
for the cap, A11 (30/25/20/15/10) and A12 (the same with a real 4% and 1%
tail); the band targets and R11 are now the cap, not the old concentration
arc (design doc 2.5 rewritten). `apply` writes rod and surf tables from a
five-species cast with a level range (`layout.water`). `dex.final_by_level`
reads the evolution levels for the cap rule. The availability plan gained
`tail` per area, `corridor_splits` in place of the order cut, captures per
(split, location) on every line, and a cap-candidates list for Ian; its
document has a capture-areas section. `encounters_verity_lakefront.json`
exists and is in the NARC, a new capture area; its header still points at
no table and the map has no grass (backlog, script track). Seven rows
joined the pick-list (Nosepass, Geodude and Phanpy lines) and Makuhita's
line moved to starter-adjacent.

**The second review, the same day.** Old Rod additions approved bar Psyduck
(Goldeen, Corphish, Chinchou, Carvanha, Remoraid, Buizel, Shellos: fourteen
rows on the list, starter-adjacent), starters in the rod tails too; caps
for every split (Roark 16, Gardenia 26, Fantina 33, Maylene 38, Wake 44,
Byron 53, Candice 56, Volkner 62, League 78); a delay is worth taking for
several starters or value lines at 10-20%, not for a 5% tail; Route 211
west is the early version and 211 east the delay; Riolu (the Iron Island
egg) and Eevee (Hearthome) are already guaranteed, so out; no fixed share
split, "variety is the spice of life"; and Platinum Kaizo's tables as the
model. Those turned out to be the base ROM's own tables, line for line
(platinumkaizotracker.com/locations against the tree before this step), so
the reference was already here: ten distinct species a grass table, one per
slot, two more by day and two by night, starters in the grass as a delay's
reason (Route 204 north: Bulbasaur 20, Chikorita 24, Treecko 10) and in the
Old Rod tails, a core cast repeating across neighbours at different shares.
Design doc 2.5 carries that note.

**The tables, second cut.** Seven shapes joined the archetype table
(A13-A19; A19 is Kaizo's own, twelve distinct lines with real 4s and 1s)
and the twenty land tables use seven different ones, eight to sixteen lines
each with distinct day and night pairs, no species over 25%. Route 204
north is the delay: Scorbunny at home at 25, Treecko 20, Snivy 10, Torchic
by day at 10. Route 211 west is plain (Bronzor, Vulpix, Mienfoo co-equal);
Route 211 east is planned as the next delay with Ralts, Rowlet and Litten,
to author with Byron's split. Every classic starter on the list is wild in
the first two splits (Charmander and Litten as Route 207's 1%s, Torchic on
203 and 204 north, Treecko on 204 north, Mudkip on the lake and in three
rod tails, Squirtle in three rod tails) and none is a home. The fourteen
Old Rod tables use the new lines and end in a starter at 4% or 1%. The
availability plan lists a gate-tier starter as a cameo or tail, never a
home; the first split's tier rule stands; early tables want 5-16 lines.

**Numbers.** Per-table lint 0 errors on the twenty. Game-wide R12 is 59
errors, all pool lines and later-split placements; the cap-candidates list
now reads the later caps too and names 21 lines for the later splits
(Koffing, Yanma, Sneasel, Slugma, Swinub and on), which Step 4 takes up.
Suites 35/35, 21/21, 18/18, 28/28, run one at a time: `test_step0` rewrites
shared files under a restore and cannot share the tree with another suite.

**An interpreter fault, not a tool fault.** `test_step0` fails on a random
file now and then, and chasing it landed on this machine's Python 3.14.4:
the same string work on the same text gives different answers after a few
hundred repetitions, with no writes and no threads. The minimal case is
`tools/oxide/python_flake_repro.py` (its docstring has what was ruled out:
hash seed, JIT, the C json scanner, the allocator). Until the box has
another Python, a failed `test_step0` with a KeyError, "unbalanced
container" or "'int' object is not callable" in `jsonstyle.py` is that
fault; rerun it. Ian's call whether to report it upstream.

*Gate:* per-table lint clean, done; the plan's gate passes with the splits.
Still open: the merge into `oxide`. Ian took his playthrough off the gate
(2026-09-21, far too long); his review happens in the tool, which now lists
the water-only areas (Twinleaf Town, Route 219) beside the grass ones.

### Step 4 — the rest of the game — **written, 2026-09-21; merged into `oxide` 2026-09-21**

```
PYTHONPATH=. python3 -m tools.oxide.encounters.cli apply --all --dry-run   # 184 areas, 0 failed, nothing to change
PYTHONPATH=. python3 -m tools.oxide.encounters.cli availability            # the gate, passes
PYTHONPATH=. python3 -m tools.oxide.encounters.cli lint                    # errors are R12's pool lines only
PYTHONPATH=. python3 -m tools.oxide.encounters.test_step3                  # 28/28
```

**What was written.** Every remaining live land table, 152 of them, split
by split from Fantina to the post-game, and every water table: surf (from
Byron's split, the HM from Celestic; the sidecar's `splits.rods` now gates
surf too), Good Rod (from Maylene's), Super Rod (from Candice's) and the
Old Rod where it was not yet designed, 198 tables over 53 areas. The land
follows the plan's homes (Ian approved the first two splits' feel, so the
same width and cap continue: eight to sixteen lines a table with distinct
day and night pairs, seven to eleven shapes in rotation, nothing over 35%).
Room groups (Old Chateau's nine, the Lost Tower's five, Solaceon's
eighteen, the Great Marsh's six, Iron Island's seven, Mt. Coronet's
eleven, Victory Road's six, Snowpoint Temple's six, Stark's three, Turnback
Cave's twenty-two plus the twenty-five unreferenced post-game files) draw
on one pool each with shape and order rotating so no two rooms read alike.
The water is four regional pools (river, sea, marsh, mountain) rotated per
area with a starter in every rod and surf tail (Squirtle, Mudkip, Froakie,
Popplio; their middle stages on the Super Rod), levels stepping by split,
and the plan's water homes pinned into the first slots.

**Delays and the cap rule.** Route 210 north (Hawlucha, Goomy, Fennekin and
Litten by day) and Route 211 east (Ralts and Ferroseed at home, Rowlet 20,
Litten 15, Jangmo-o 10) are the next delays after 204 north. The
cap-candidates list drove placements: Koffing and Glameow on Route 209,
Yanma on 215, Swablu, Sneasel, Slugma and Fennekin on 210 south, Swinub on
214, Joltik and Salandit on 206, Ferroseed in the Maniac Tunnel, Goomy on
210 north, Jangmo-o on 211 east, Larvitar on 217, Trapinch on 221, Galarian
Mr. Mime in the Trophy Garden. Three remain, listed for Ian: Snorunt and
Snover (final by 42 and 40, cap Wake 44, first Candice: the cold lines have
no warm home, so this is his call), Larvesta (final by 59, cap Volkner 62,
first Post: Stark Mountain is post-game). The four Kanto and Hoenn starters
on the list are now wild in every region as 1%s and 5%s; the eight new
starters sit at real shares where planned.

**Pick-list and rules.** Mantyke is not on the list after all (the earlier
inventory line was a mapping artefact), so the sea pools carry Tentacool,
Finneon, Luvdisc, Remoraid, Mareanie and Shellos. R8's spread floor moved
from 2.2x to 1.8x: 2.2x was vanilla's with its concentrated early routes,
and under the cap every table is flat (the game reads 1.99x).

**Numbers.** 172 live land tables and 198 water tables designed; the plan's
gate passes (home 95, non-wild 51, water 14, honey 3, cameo-only 2, pool
20, proposed 2); game-wide lint errors are R12's 22, the pool lines and the
two proposed statics, which the pool's scripting settles. Land, day/night
(bar a residue), surf and rod slots hold no off-list species; swarms,
radar, the dual-slot lists, the honey trees, the marsh lookout and the
garden dailies are Step 5's.

*Gate:* game-wide lint 0 errors bar R12's scripted lines, done; R8, R9, R11
pass; the merge into `oxide`.

### Step 5 — the no-leak pass — **done, 2026-09-21**

```
PYTHONPATH=. python3 -m tools.oxide.encounters.cli audit --summary --fail-on-leak   # exit 0, 0 off-list outside scripts
PYTHONPATH=. python3 -m tools.oxide.encounters.test_step5                            # expect 16/16
```

**What was written**, by an Opus subagent on a brief from this track, and
checked here. Every key of every encounter file now holds on-list species:
swarms (the route's own face evolved where the level warrants, else a
neighbour's line, never something the table already shows), the Poke Radar
four (the route's lines evolved, Luxio first where Shinx is at home), the
five dual-slot lists (Hoenn lines to Ruby, Sapphire and Emerald, Kanto to
FireRed and LeafGreen, within twenty levels of the route), the day and night
residue (`SPECIES_NONE` in the twelve rate-zero files), the twelve rate-zero
land tables (each a slot-for-slot copy of its nearest designed table, so no
level-0 `SPECIES_NONE` slots remain), the honey trees (the plan's tiers:
rare Rowlet, Snivy, Sprigatito; uncommon Combee, Heracross; common Combee,
Sewaddle, Grubbin), the Great Marsh lookout (32 and 32 from the marsh's land
and water lines) and the Trophy Garden dailies (sixteen, the garden's cast
plus four). Three writers joined `model.py` for the species-only files
(`set_honey_tier`, `set_marsh_lookout`, `set_daily`). The audit reads 7046
references in 186 files, 0 off-list; the scripts section still lists its 42
off-list gifts and statics, which decision 8 leaves to the script track.

**A note on what these lists are worth.** Ian has said elsewhere that
swarms, the Poke Radar, the dual-slot lists and the Trophy Garden dailies
are not used in Oxide; they are filled so that nothing off-list can ever
be rolled, not as acquisition sources, and the availability plan counts no
capture from them.

**A test that ate a table.** `test_step0` restored its scratch file with
`git checkout --`, which in a shared checkout with uncommitted work throws
away everything else in the file: it reverted Route 214 to the base ROM's
table once. Both places now snapshot the file's text and write it back,
and `test_step5` does the same. Route 214 was re-applied from its sidecar
entry; `apply --all --dry-run` reports nothing to change on all 184.

*Gate:* `cli audit` reports 0 off-list references outside scripts, done.

### Ian's follow-ups after Steps 4 and 5 — **done, 2026-09-21**

Ice earlier, on and beside Mt. Coronet: Alolan Ninetales is at home on
Route 211 west at 20 and by night, with Snover at 10; Mt. Coronet's first
room (Gardenia's split) carries Snorunt and Alolan Ninetales at 10 with
Swinub and Snover behind; the south entrance has Snom and Swinub at 5 and
Snorunt by night. The tree has no separate Alolan Vulpix and does not need
one: the Alolan Ninetales here evolves from ordinary Vulpix, which is on the
list and in the early tables already (Ian, 2026-09-21, closing the port
question this entry first raised). Larvesta's
home moved from Stark Mountain to the Fuego Ironworks at 10. Mantyke and
Mantine are back on the list (rows 386 and 387) and in the sea pools, Route
219's and 223's surf pinned. The cap-candidates list is empty.

**The sources catalogue is this track's now.** `docs/oxide/pokemon-sources.md`
and `.csv` (from `tools/oxide/pokemon_sources.py`, Ian's handoff) join the
availability view: every line's catalogued sources are a column of the Lines
table, and a gift, egg, trade, static, fossil, roamer or starter row counts as
a non-wild source where the script scan found none. Regenerate the catalogue
after any table change (`PYTHONPATH=. python3 tools/oxide/pokemon_sources.py`).
It also records what stays off-list on purpose: the eighteen Unown rooms of
Solaceon Ruins (Unown stays off the list, decision 9, Ian's call of
2026-09-21) and the thirty-odd clown-gift rows, the script track's levers.

### Step 6 — build, verify, merge — **done, 2026-09-21**

`integrate.sh` merged the branch into `oxide` (a fast-forward of ten commits) and
ran the full gate: 25 checks green, `verify_narcs.py --encounters --source` at
183 of 183 tables, every suite passing. One check failed on the first run and was
fixed before the push: `import_base_rom.py --dry-run` wanted to restore the base
ROM's surf and rod species on the eleven water-only areas Step 5 authored, because
its definition of "authored" was a sidecar entry with a land `cast`, and a
water-only area has none. A sidecar entry with any of `surf`, `old_rod`,
`good_rod` or `super_rod` now counts too, and `test_step0` asserts the same. The
lesson is in the design doc's findings log: a new way of authoring a table has to
extend `authored_encounters()` or the gate quietly reverts the tables.

### Step 7 — the scripted sources, and four notes from Ian — **done, 2026-09-21**

**The gifts are encounters now.** Ian's instruction was to sort the scripted
sources into buckets by the source rather than the row, to treat each bucket as
an even-odds pool, and to replace every off-list member. Fourteen gift sources
are re-pooled, the whole design and the reasoning per town is in
`docs/oxide/encounters/scripted-sources.md`, and the catalogue's off-list count
falls from 37 species to 8. What is left is flagged there rather than changed:
the Oreburgh and Eterna trades, the Day Care's Ditto, the museum's four spare
fossils (the list has three fossil lines and the machine revives seven) and
Chimchar, which Rowan still offers although the list does not have it. Pastoria's
roll is the only behaviour change: six gift branches existed and the roll only
ever reached three, so it was widened to six. Twelve scripts and two text banks
now diverge from the base ROM on purpose, which `bulk_scripts.py`,
`import_base_rom.py` and `bulk_text.py` have each been told about; `bulk_text.py`
had no skip list at all before this and now honours the importer's.

**Solaceon Ruins is one table.** All eighteen rooms carry the same cast, because
in game there is no way to tell which room is which and eighteen different tables
were eighteen ways to guess wrong. Klefki keeps its home in room 2 and the other
seventeen hold the same twelve lines without claiming it. Hippopotas is in that
cast at 5% rather than dropped, because it is fully evolved by 34 and Maylene's
cap is 38, which is Ian's rule for when a line has to be catchable.

**Sendoff Spring is the high-value table**, at Ian's request: Gible, Beldum,
Larvitar, Goomy and Jangmo-o carry it, with Absol, Sneasel, Scyther, Ralts,
Heracross and Elekid behind and Dhelmise keeping its home. Its split moved from
Post to League on the reading that the spring itself needs only Surf and
Waterfall, and that it is Turnback Cave inside it that is post-champion. If that
reading is wrong the table is still fine; only the split label moves.

**Two lines joined the pick-list**, Gastly and Misdreavus (rows 388 to 392), to
answer Ian's note that the Old Chateau was thin on ghosts. The Chateau's nine
rooms are rewritten around six ghost lines, Gastly at home in the corridor and
Misdreavus in the side rooms. A side effect: the Snowpoint Gengar trade is on the
list now, so it is no longer one of the flagged trades.

**Out of scope, on Ian's word (2026-09-21): anything post-champion.** Turnback
Cave, which is the whole of the Post split bar Sendoff Spring, is not reachable
before the champion without script work, so its tables stand as they are and are
not worth more design time.

**Then a second round of notes the same evening.** The gifts are all flag-guarded
now, one flag each, checked on the way in and set after the Pokemon is handed
over so a full party does not burn the chance; thirteen spare flags at 0x03BF in
`generated/vars_flags.txt` were named for them, which is safe because that list
is positional and nothing referred to any of them. The four spare fossil items
are to be deleted rather than repointed, which is item and script work in the
backlog. And Chimchar is answered rather than flagged: Rowan's briefcase offers
**Scorbunny**, so all three options are on the list. That is one define in
`src/choose_starter/choose_starter_app.c` and the rival and counterpart mapping
in `src/system_vars.c`; the rival's trainer files are named for the player's
choice rather than the rival's species, so none of them needed touching. Scorbunny
left the wild in the same move, being gate tier now: Litten took its home on
Route 204 north, Route 207's 1% Litten tail became Torchic so the delay prize is
not already catchable in Roark's split, and Route 206's 1% Scorbunny tail became
Froakie.

Gate after all of it: plan gate green with 0 cap candidates, `lint --ignore R12`
0 errors, `audit --fail-on-leak` exit 0, and the suites at 35/35, 21/21, 18/18,
28/28, 16/16, 13/13, 23/23, 18/18, 46/46, 15/15 and 19/19. The catalogue's
off-list species are down to seven: the Unown rooms, the four spare fossils and
the two Dittos and the Chatot of the flagged trades.

### Step 8 — stages, trades and the last two menus — **done, 2026-09-21**

**Every wild slot now holds the stage its level deserves**, which is Ian's rule
of the same day and the largest single change the tables have had: an Elekid at
Sendoff Spring is an Electivire, Treecko and Snivy on Route 208 are a Grovyle and
a Servine. It is a command rather than a one-off script, `cli evolve`, because it
has to be re-run whenever a table's levels move: it reads the written tables for
levels, so it runs after `apply`, writes the sidecar and the plan, and then
`apply` writes the tables. Three rules decide a slot, and the middle one is the
one worth arguing with:

1. A species is judged by the **lowest level it appears at in that area**, and a
   water slot by the floor of its range, so nothing evolves until the whole slot
   has.
2. **A line that grows up on its own grows up at its own level.** Where a stage
   has any level-up evolution, the stone and trade routes out of it are ignored.
   Without this Snorunt would become a Froslass at the stone's judged level and
   never reach Glalie at 42.
3. A method with no level of its own is **judged**: friendship at 20, a stone at
   30, a trade at 38. That last number is what makes Electabuzz an Electivire
   late and not before, and it is Ian's own example.

Where a line branches into two stages that are both available, `BRANCH` in
`evolve.py` picks: Ceruledge over Armarouge, Scizor over Kleavor, Gardevoir over
Gallade, Glalie over Froslass, Cofagrigus over Runerigus. An unruled branch stays
put rather than guesses. An evolution into a species the pick-list does not carry
is refused, and so is one whose stage is already in the same table, which is 51
slots: those are tables that deliberately hold two stages of one line, the way
vanilla holds Geodude beside Graveler.

Two bugs in the pass are worth recording because both hid in plain sight. Water
rows key their levels `level_min`, not `min_level`, so the first run judged every
water slot at level 0 and quietly evolved nothing in the water. And a water-only
area keeps a land array at rate 0 that the sidecar has no cast for, so judging it
asked for a change that could not be written and the pass never converged. Both
are fixed, and `cli evolve` now reports zero moves on a settled tree, which is
the check that it has converged.

**The trades are rebuilt** and **the last two list menus roll**; both are
described in `docs/oxide/encounters/scripted-sources.md`. The trades needed the
engine: the level a trade hands over is the level of the Pokemon the player gave
up, which stops making sense once the trade takes anything, so a small table in
`src/overlay006/npc_trade.c` names a level per trade with 0 keeping vanilla's
behaviour; and vanilla asserted that a trade is never shiny, which two of ours
now are on purpose.

**The Day Care's gift** was to become a shiny winter Sawsbuck; neither Deerling
nor Sawsbuck is in the species tree, so Ian moved it to a **shiny Floette** with
the same perfect IVs and neutral nature at level 30, and ruled breeding out of
scope, which is what losing the game's only Ditto costs. That needed the fork's
second script command. `GivePokemon` rolls the personality value, and therefore
the nature, and rolls the IVs; `GiveDesignedPokemon` takes a nature, one IV value
for all six and a shiny flag, and builds the personality to satisfy the nature
and the shininess at once, the same arithmetic the rebuilt trades use. Like
`GiveHiddenAbility` it is registered at the end of `scrcmd.h` so no existing
opcode moves, and `audit.py` and `pokemon_sources.py` both read it now.

The white flower is the one part still missing. Floette's colours are forms and
this tree has a single Floette with one sprite and one palette, so a white one is
art and a form record rather than a number in a script. Backlog.

Gate: `cli evolve` 0 moves, plan gate green with 0 cap candidates, `lint --ignore
R12` 0 errors, `audit --fail-on-leak` exit 0, a full `make rom` clean, and
`verify_narcs --encounters --source` at 184 of 184 tables. Suites 35/35, 21/21,
18/18, 28/28, 16/16, 13/13, 23/23, 18/18, 46/46, 15/15, 19/19.

### Ravaged Path is Roark's split: 2026-09-22

Ian's correction: Ravaged Path is reached before Roark's badge, so the whole
area belongs to Roark's split, where only its Old Rod had been counted before.
`progression.py` moved it and `test_step3` pins the new boundary. Roark's split
may hold only starter-adjacent lines, scripted ones and 4% or 1% tails, and the
plan's gate caught Wooper, a preferred-tier line in a 5% grass slot. Lotad took
that slot, which keeps the table's approved shape and its wet corner. Wooper is
still catchable there in Roark's split, since the Old Rod carries it. The
no-leak pass followed the change into Oreburgh Mine B2F's swarm field, which
Oxide never uses.

### Ian's notes on the Tables view: 2026-09-22

Play order had been sorting by each area's median level, which put Twinleaf Town
after Route 219 and scattered splits (Wayward Cave away from the rest of
Fantina's). `/api/areas` now gives each row its split's position and its sidecar
`order`, and the page sorts by split first, Post last, then by that order.
Within a split the sidecar's order stands, so Route 219 (order 92) closes
Roark's split.

The twenty-five `unknown_533` to `unknown_557` files are parked out of the
browser tool until something uses them: gone from the area list, the header's
game metrics and the dex's "where it is met". The CLI, the linter and the
availability plan still read them. `test_m4` expects 159 areas now.

In the centre, party icons are drawn at 64px (rows 68px), and "What a player
meets" sits beside the slot table with its rows level with the slots, each line
two rows high: name and both odds on top, the bar across the full width
beneath. Ian then asked for the list's heading and the slot table's own "Real
odds" column to go, since the list shows real odds and the heading pushed its
rows out of line. The two sit side by side when the window is about 1880px wide
or more and stack below that. Ticking a catch now eases those bars to their new
lengths over 350ms, as the repel ladder already did, instead of jumping.

Every font size in the page went up 2.5px (base 16px, centre 18px), and the left
pane widened from 420px to 460px with wider number columns so the level range
and catch count no longer collide.

One bug Ian found along the way: that list showed the morning table's odds
whatever time of day was picked. The server built it from the base slots only.
`/api/area` now also sends `merged_layers`, a day and a night list with their
two species in slots 2 and 3, and the page shows the one for the chosen time;
the bars ease between times as they do on a catch. The planner's species menu
still reads the base list, which is what it plans against. `test_m4` gained a
check for the day and night lists and one for the split ranks (49 checks).

A second note the same day: area names were cut short in the list, and the last
two numbers had no labels. Each list row now gives the name its whole first
line and puts the split tag, the catch, the levels and the two numbers on the
second. A header row names those columns, with an explanation on hover: Left
is the species still needed out of all the area's species, and Best odds is
the best chance of meeting the rarest of those with the best repel lead. Area
names are capitalised everywhere the tool prints one (floors as 1F and B1F,
"Mt." and "Pokémon" spelt as the game spells them), and the search box
also matches the file name, so "mt coronet" still finds Mt. Coronet.

### The QA pass before the merge: 2026-09-22

The Overseer's `/qa-pass` over this branch
(`docs/oxide/qa-review-2026-09-22-encounter-m8.md` on `oxide`) found two dex
defects, one gap in D5's plan and two nits, all in this track's files and none
blocking. All five are dealt with:

1. Nidoran♂ was taken for a mega, because any constant ending in `_M` was.
   A mega now needs its base species to exist, so Gyarados and Lopunny keep
   their megas and Nidoran♂ is back in its own line.
2. Evolution lines were sorted by name (Incineroar, Litten, Torracat). The
   server now walks each line from the member nothing evolves into and marks
   every member's stage; the page draws one group per stage, so Eevee's eight
   evolutions sit side by side after Eevee.
3. The calculator is not offline as vendored. D5's plan above now lists
   everything its patches have to remove, not only the data loader, and
   `calc/VENDORED.md` says the same.
4. The dex's caches outlived hand edits while the server promised nothing was
   stale. Species, the species list and moves are now cached against their
   files' modification times, so an edit shows on the next request.
5. A bare `/api` answered 500. It, and `/api/area`, `/api/move` or
   `/api/sprite` without the name they need, now answer 404.

`test_m8` has three new checks (46) and `test_m4` one (51). The review's figure
for R12 is right: 27 scripted lines, up from the 22 of Step 4 as Steps 7 and 8
re-pooled the gifts; the tracker says so now. Its question about Steel's two
Generation 4 resistances went to Ian, who ruled the same day to keep them: the
chart stays as it is, and `test_m8` pinning Steel's resistance to Dark and
Ghost now guards a decision rather than a finding.

A third note, drawn as a sketch: more of an area on one screen. The heading
above the tables is three short lines now (name, tags and the encounter on one;
the note; the table and time-of-day tabs on one row). Grass rows are 46px with
the 64px icon overhanging, which makes the twelve slots about as tall as the
odds list beside them. Underneath, the area's water tables sit four across in
brief (each slot's rate, icon, species and levels, with its real odds on
hover), drawn from a new `water` list in `/api/area`. A panel is a view:
clicking it opens that table above for editing, as its tab does, and the one
being edited is outlined. `test_m4` checks the water list (50 checks).

## M8, the dex and the damage calculator: **D1 to D4 done 2026-09-22, D5 next**

Ian asked to pull the things `ddex` (https://ddex-chi.vercel.app/, source at
`hzla/ddex`) and its damage calculator (`hzla/Dynamic-Calc-Decomps`) do into this
tool: a species viewer with sprites, base stats and what changed from vanilla,
learnsets, and a calculator that knows Oxide's numbers. His four rulings, given
before any of it was designed: build it **into this tool** rather than feeding
ddex, go as far as a **full local calculator**, treat it as **an instrument for
him while authoring** rather than something players see, and cover **all four**
surfaces (stats with deltas, learnsets and moves, sprites, encounter
cross-links).

### What the survey turned up

**ddex reads a Gen 4 hack by uploading an `.nds`**, which `make rom` produces
every time, so that looked like a free second opinion. Ian tried it on
2026-09-22 and it half works: much of the Pokedex, the encounter tables and the
location names come back as garbage. That is the expected failure and it is worth
writing down, because it is the argument for this milestone. A parser written for
vanilla Platinum assumes vanilla's shapes, and Phase 4 moved all three of them:
the species archives hold 667 members rather than 508, the species record grew
from 44 bytes to 48 when the abilities became `u16`, and the evolution record
grew from 44 to 56, so reading them at vanilla's stride walks off the end of
every record after the first. Location names are a message bank whose indices
moved for the same reason. Nothing in ddex is wrong; it simply cannot know what
this fork did, and no upload will fix that.

The lesson for us is that reading `res/` is not merely more convenient than
parsing the ROM, it is the only source that is correct by construction: the JSON
is what the build consumes, so a viewer built on it cannot drift from the game.
ddex also already does wild encounters with nuzlocke routing and dupe tracking,
which overlaps this tool; what it cannot do either way is know our design data,
which is why the cross-links below are the part worth building rather than
borrowing.

**The licences differ and decide what may be copied.** `Dynamic-Calc-Decomps` is
MIT, so vendoring it is clean as long as its licence travels with it. `hzla/ddex`
has no licence file at all, so none of its code comes into this repo without
asking him first. Nothing here needs it.

**The calculator is static files.** `index.html`, `js/`, `css/`, `calc/` and
`data/`, served directly by GitHub Pages with no build step, so it can be vendored
and served by our own Python server without adding node or npm to this project's
build. It takes its game data as a JSON blob in Showdown's naming, which the
hosted version fetches from npoint.io. Feeding it ours is a data export, not a UI
job, and pointing it at our server is the one patch it needs.

**Everything the dex needs is already in `res/`.** Each species' `data.json`
holds base stats, types, the three abilities, evolution methods and the level-up
learnset; `res/moves/` holds 469 moves with class, type, power, accuracy, PP,
priority and flags, which is everything a damage formula wants; sprites are
ordinary indexed PNGs a browser renders as they are (160x80, two 80x80 frames
side by side) with a party icon beside them; and the vanilla baseline for "what
changed" is `git show main:res/pokemon/<name>/data.json`, the same trick the
linter already uses for tables. No ROM parsing, no uploads, no network.

### The milestones

**D1, the data layer — done, 2026-09-22.** `pokedex.py` beside `dex.py` (which is
about pick-list lines and keeps its name): all 652 species with stats, types,
abilities, evolutions and learnsets, 468 moves with what a damage formula reads,
sprite paths, the type chart, and the vanilla delta for anything that existed on
`main`. New species have no vanilla row and read as new rather than as changed.
`captures()` is the cross-link the dex exists for: from a species, every table,
kind, location, split, share and level range it appears in, taken from the tables
themselves rather than from the design, 248 species over 1,060 water appearances
and the land besides. Endpoints: `/api/dex`, `/api/dex/<species>`,
`/api/move/<move>` and `/api/sprite/<folder>/<kind>`, which serves the PNG out of
`res/`. Gate: `test_m8`, 23 checks, green.

Two things worth knowing came out of it. Clefairy is the reminder that the delta
is worth showing at all: it is Fairy now and it lost Cute Charm, neither of which
any note in this repo mentions. And **the type chart is this fork's own**, which
is the next item.

**The type chart, checked against the ROM on Ian's hunch.** He guessed it might
have Fairy while keeping Generation 4's Steel, and it does. Read out of
`sTypeMatchupMultipliers` in `src/battle/battle_lib.c`: all eighteen types, Fairy
complete and correct (strong on Dragon, Dark and Fighting, weak to Poison and
Steel, immune to Dragon), and Steel still resisting Dark and Ghost, which
Generation 6 took away. So no stock `types=` setting in the calculator matches:
Generation 4's has no Fairy and Generation 6's drops those two resistances. The
chart therefore travels with the exported data rather than being named by a
parameter, which `pokedex.type_chart()` already reads from the source of truth so
it cannot drift if the table is edited again. Keeping those two resistances was
never decided when Fairy was ported; Ian decided it on 2026-09-22: Steel keeps
them.

**D2, the dex tab — done, 2026-09-22.** The page has two views now, switched
from the header, and the tables view is untouched. The dex list draws a party
icon, the name, the types and the base-stat total with its change from vanilla,
filtered by a search box that matches names or types and by four buttons: all, in
tables, changed, new. The species page carries the front sprite, the types, the
dex entry, base stats as bars with each stat's delta beside it, the abilities
with the hidden one marked and vanilla's listed when they differ, the whole
evolution line with how many tables each stage is in, and the level-up learnset
with each move's type, class, power and accuracy. The right pane answers where
it is met, grouped by grass and each rod, with the location, the split, the share
and the level range, and what every type does to it.

The line view is there because the cross-link is per species and has to be: after
the evolution pass a table that used to hold Litten holds Torracat, so Litten's
own page says one table while its line says five. That is the truth rather than a
wrinkle, but the page has to show both halves of it or it misleads.

Two details worth recording. The sprites are frame sheets, a front or back being
two 80 by 80 frames side by side and a party icon two 32 by 32 frames stacked, so
the page crops to the first. And they carry no alpha at all: the colour the game
treats as transparent is simply palette entry 0, which a browser would draw as a
beige box, so the server adds the `tRNS` chunk that says so as it serves them.
That is 28 bytes and it leaves the file on disk alone.

**Running two copies at once.** There is a copy of this tool in every checkout
and worktree, they all want port 8765, and a page served from the wrong one is
indistinguishable from a view that was never built, which is exactly how the dex
first appeared to be missing. Three changes so that cannot happen quietly: the
header names the checkout it is reading, a taken port says so in a sentence and
suggests the next one rather than unwinding a stack trace, and `--port` lets a
branch and what is merged run side by side. Nothing the server sends is
cacheable now either, for the same reason.

Gate: `test_m8` at 30 checks, including every pick-list line opening with all
twelve fields the page draws and a party icon to draw beside it. The two `cut`
rows, Toxel and Toxtricity, are excluded by name: they are on the sheet and
deliberately not in the tree, because their evolution depends on nature and
Generation 4 has no method for it.

**D3, sprites in the tables — done, 2026-09-22.** A party icon sits beside every
slot in the table being edited and beside every line of what a player meets, from
the same endpoint the dex uses. The page works the sprite out rather than being
told: a species' folder is its constant lowercased, which holds for all 652, and
`test_m8` checks that every species any table holds has an icon to draw, so a
table naming one it does not hold for is a failing check rather than a broken
image in the middle of a table. A slot showing a day or night substitution draws
the substituted species, not the morning one. Anything already caught draws its
icon faded, which is the same "absence rather than another colour" the rest of
the view uses.

The left list is deliberately untouched: its species column is the caught
encounter, which is empty for most rows, so icons there would be mostly blank
space.

**Then a pass against ddex's own dex, on Ian's comparison.** Three bugs of mine
and two features.

The bugs. The stat bars drew as empty boxes, because the cell borrowed the
existing `.bar` class, which is the repel ladder's bordered 22-pixel row.
Twelve species read as `-----`, because the alternate-form records carry a
placeholder name, a form being named after its base in game; one of them is
Alolan Ninetales, which is at home on Route 211 west. And a mega listed as a
stage of its line, twice, once for each of the day and night methods an
alt-evolution is entered under.

The features. Stat bars are banded by value the way a dex bands them, muted
enough to sit beside the teal. And every line of "where it is met" opens that
table: the dex knows which area, kind and split it means, so it switches view,
selects the area and picks the right rod. That is the cross-link working in both
directions, and it is the thing no general dex can do.

**A second baseline, and a trap avoided.** Ian's other note was that the ported
species do not compare against anything: `main` has never heard of Annihilape,
so the dex said "new" and stopped. `canon.py` fixes that by comparing every
species against its real Generation 9 self, and the same map from our constants
to Showdown's spellings is exactly what D5 needs, so it is written once and
tested here: all 652 land on a canonical entry.

The trap: the obvious source was the species table inside the vendored
calculator, and it is **not canonical**. It ships whatever data it was last
built with, and the calculator loads the real thing at runtime, so its table is
some romhack's: Arbok as Dark/Poison, Lapras as Dragon/Water, Lopunny as
Normal/Fighting. Comparing against it would have had the dex report 27 type
changes this project never made. The baseline is upstream `@smogon/calc 0.12.0`
instead, vendored at `canon_src/` with its provenance, and `test_m8` pins those
three species so a regeneration from the wrong file fails loudly rather than
quietly lying.

What it says now is worth reading: 470 of 652 species match canon exactly, 181
differ in stats, which is the base ROM's own buffing (Slugma and Surskit both
+140, Spinda +120), and **three differ in type**: Galarian Rapidash is Fairy/Fire
here against Fairy/Psychic, Gothitelle is Dark/Psychic against Psychic, and
Tsareena is Fighting/Grass against Grass. Those three are either deliberate or
import slips, and either way they were invisible until now.

**D4, moves: done, 2026-09-22.** A third view, Moves, beside Tables and Dex.
The list holds all 922 moves with type, class, power, accuracy and how many
species learn each, filtered by a search over name, type or effect and by five
buttons: all, learnt, changed, new, unscripted. A move's page gives its numbers,
target, effect with its id, the machine that teaches it, its flags, and a table
of every field that differs from vanilla. The right pane is the reverse index:
every species that learns the move, by level-up, machine, tutor or egg, sorted
by level and then by the earliest split the species is met wild. Every name is
a link. A learner opens its dex page, and the dex page's level-up moves, plus
new lists of its machine, tutor and egg moves, open the move. A jump from one
view clears any filter that would hide the row it lands on.

Three things the page knows that the move files do not say directly:

1. **Which moves are unscripted.** Element 4 gave the donor's effects 277 to
   406 placeholder scripts, a copy of either effect 0's plain hit or Splash's.
   `pokedex.stub_effects()` finds them by comparing the scripts, so an effect
   stops being flagged as soon as its real script lands, with no list to keep.
   Today that is 130 effects and 136 moves. The list marks them with the lint
   warning's dot, and the move page says what the player will see: the damage
   without its extra, or "But nothing happened!" for a status move.
2. **What changed from vanilla**, per field. 190 natives differ. Most of them
   (96) differ only in the King's Rock flag element 4 gave every damaging move.
   The rest are the base ROM's own edits: Tackle's accuracy, and Attack Order
   rebuilt as a 120-power poison hit. Charm's Fairy retype shows too. The
   baseline is `main` read in one `git cat-file --batch` call rather than 468
   `git show` calls, which keeps the list at about 70ms.
3. **Who can use it, and from when.** 464 of the 922 moves are learnt by at
   least one species. Most of the other 458 are new moves nothing learns yet,
   because refilling the new species' learnsets is element 4's last piece, and
   the move page says so rather than looking broken. A machine is read from
   its item record (`res/items/data/tm02.json` teaches Dragon Claw), so the
   index follows any change to the TM list.

Gate: `test_m8` at 59 checks, thirteen of them D4's. None of them pins a count
of placeholder effects, since element 4 will bring it down; they pin what a
placeholder can and cannot be instead. The page was rendered in a headless
Windows Chrome in both themes with no page errors, and the jump from Gible's
egg moves to Outrage was driven through and landed on the right row.

**Ian's notes after D4: 2026-09-22.** A species in a table now opens its dex
page. The name in a slot is the slot's editor, so the way through is the party
icon beside it, and the same goes for the icons in the water panels and the
encounter heading. In "what a player meets" the name itself is a link. The
tables view catches these clicks on the way down, so a water panel's own click,
which opens that table for editing, never sees one.

There is a Back button too, and it is the browser's history rather than a
stack of the page's own. Every place the page can show (a view, plus the area
and table, species or move in it) is a history entry with the place in the URL,
such as `#dex/SPECIES_GIBLE`. So Back, Alt+Left and a mouse's back button all
retrace a path like table, species, move, another species, and a reload opens
where it was. Driven through in a headless Chrome, back and forward and after a
reload, with no page errors. `test_m8` is at 60, the new check pinning the
wiring, since no endpoint can see it.

**D5, the calculator.** Vendor the MIT calc under `tools/oxide/encounters/calc/`
with its licence intact, generate its data from `res/`, serve both from our
server. The work is the export, in rough order of difficulty: a naming map from
our constants to Showdown's spellings, with the awkward cases being the regional
forms, the megas, Mr. Mime, Jangmo-o and the Tapus; species entries with stats,
types, abilities, weight and gender ratio; moves with category, power, accuracy,
priority and the flags the formula reads; learnsets so the set builder offers the
right moves; and a patch to its loader so it reads from `localhost` instead of
npoint. That one patch is not enough to make it offline, which the QA pass of
2026-09-22 found: as vendored, the page also loads jQuery and other libraries
from Google's, jsDelivr's and unpkg's CDNs, a Google Tag Manager analytics tag,
and game data from `hzla.github.io`, about 100 remote references in all. D5's
patch list has to vendor or drop every CDN script, remove the analytics tag and
remove every remote data URL, and its gate includes the page loading with the
network off. Gate: a hand-checked damage roll against the game, the export
regenerating clean after a species edit, and no request leaving the machine.

### Decisions and risks, recorded before starting

- **Mechanics settings: settled, and not what it looked like.** Checked against
  the ROM on 2026-09-22 rather than assumed. The chart is Generation 4 with Fairy
  added, so neither `types=4` nor `types=6` is right and the export carries the
  chart itself. Damage mechanics stay Generation 4. Still worth one real battle
  to confirm the damage side.
- **Bespoke abilities and moves.** The calculator keys its effects off Showdown
  names, so anything Hardlove invented that Showdown has no logic for will be
  inert in the numbers even when the name shows. The export should list which
  ones those are rather than let them pass silently.
- **Vendoring: decided, and done.** Ian's call was to commit it. It sits at
  `tools/oxide/encounters/calc/`, MIT, pinned at upstream `b347b337`, 12 MB over
  195 files out of a 649 MB clone; `VENDORED.md` there records what was taken,
  what was pruned and why, and the patch list to re-apply on an update. Its own
  319 MB of sprites were left behind because Oxide's are in `res/` and are the
  only ones right for this fork.
- **Out of scope for now**, and each is a small addition later: items, trainer
  teams in the calculator (the 928 carried-over teams would let a gym leader be
  checked against a party at a level cap, which is the obvious next want), and
  anything player-facing or hosted.

## The visual design, palette B: built 2026-09-22, awaiting Ian's sign-off

Ian's design for how the tool looks is `docs/oxide/encounter-tool-visual-design.md`
(palette B, Lake Guardians), mirrored by `sync-docs.sh`. It was built in the order
its section 11 gives, one commit per step: the tokens and the light and dark
toggle; every colour literal in the page replaced with a token; the pixel face and
the type scale; type chips, split tags and every "on" state moving from teal to
place; the Dex species page; and the four flavor items. The section 8 skin for the
damage calculator waits for D5, as the design says.

Every colour now lives in `ui/theme.css`, written once with `light-dark()`, and
`test_m4` gained the one check the design asks for: `index.html` and `theme.js`
hold no hex colour. `test_m4` went from 46 to 47 with it and `test_m8` stayed at
43. Pixelify Sans is vendored at `ui/fonts/` with its OFL licence and a note of
where it came from.

Four places where the build departs from the letter of the design, each because
the letter would not have done what the design wanted:

1. The theme pin. Section 3 pins a scheme by writing the `color-scheme` meta tag,
   but that tag only applies while the root element's own `color-scheme` is
   `normal`, and `theme.css` sets it to `light dark` so the page follows Windows
   with scripts off. So `theme.js` also sets the root's inline `color-scheme`,
   which outranks the stylesheet, and keeps the meta tag in step.
2. The ladder labels. Section 6 picks each label's colour with a 0.33 luminance
   threshold from the palette preview. In the dark theme that chose light text on
   the third segment at 3.2 to 1, under AA for 11px text and against section 10's
   own claim. Each label now takes whichever text token contrasts more with its
   fill, which agrees with the threshold on the other nine segments.
3. The ladder animation. Section 9 has segments ease their widths when a species
   is ticked, but a caught segment keeps its on-paper width and is only hatched,
   so a tick changes no width. The ease runs when a slot is edited instead, which
   is when widths do change.
4. Links. The design does not name them, and teal is reserved for mass, so its
   first principle makes a link neutral ink with an underline that turns to place
   on hover.

Two smaller calls. The header's metric strip is the flexible gap, so when it has
to wrap it wraps inside itself and the title, tabs, checkout and toggle hold the
first row; rendered at 1600px, the first cut had stranded the checkout and toggle
on a row of their own. And the dex number is the species' place in the tree, read
off the list the page already has, so no field was added to the API.

How it was checked, since no suite can see a colour. The page was rendered in a
headless Windows Chrome driven over the DevTools protocol, with a throwaway
profile, in both themes and both views, with no page errors. Every contrast pair
in section 10 was recomputed from the shipped tokens and matched the design's
table, as did the type chips. The toggle and the favicon were driven under node
with a stubbed browser: follow the system, pin, release, keep a pin across a
reload and a Windows switch, and survive storage that throws.

What is left is the design's own acceptance: Ian opens the tool in both themes at
his usual display scaling and signs off. The one thing only he can judge is the
pixel face at his scaling, at 16px for the title and the dex number, 13px for the
tabs and 28px for the headline; the design asks for any that look soft to move by
a pixel.

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

# Encounter Tool — Design Doc

**Project:** Platinum Oxide · **Written:** 2026-09-20 · **Status:** v1.1 (2026-09-20), amended after M1 to M4 were built against it

Two audiences. Claude Code implements sections 3-8 and 11. Ian operates sections 5 and 9,
and owns every number in section 2 and section 7 — they are house rules, not physics, and
they are meant to be edited.

**v1.1 amendments.** Building the tool measured several of this document's claims against
the files and four did not hold. Each is corrected in place below and marked *(v1.1)*:
R1 is not a description of vanilla (2.2, 7, 11); the "8% of repel tiers" figure is 24%
(2.6, 7); R11's absolute bounds are beyond vanilla (2.1, 7); R13 asks for about double
vanilla's span (7). The thresholds are now sorted into *descriptive* (vanilla passes them,
and if it does not the threshold is wrong) and *aspirational* (deliberately beyond vanilla,
so vanilla is expected to fail). The measurements behind every amendment are in
`docs/oxide/encounter-tool-build-plan.md` under M2 and M3. Water and rod tables came into
the analysis and the editor with M4 (1.4, 10). Ian accepted the R1 change and the
descriptive/aspirational split on 2026-09-20.

Companion documents, in the repo:
- `docs/oxide/encounter-design-survey.md` — the measurements every number here comes from
- `docs/oxide/encounter-tool-build-plan.md` — build order, what each milestone found, how to resume
- `docs/oxide/species-pick-list.md` — the species universe

Two earlier chat-surface notes are background only and are not in the repo:
`claude/hardlove-encounter-rewrite.md` (the previous attempt, and what it got wrong) and
`claude/hardlove-encounter-slot-rates.md` (the lesson: measurement beats internal consistency).

---

## 0. Why this exists

The Hardlove encounter rewrite produced tables that were internally consistent and
unsatisfying. Three complaints, in Ian's words:

1. Repel manips never paid. "There was effectively never a reason unless you had no
   choice otherwise to manip."
2. "Early game encounters did not *feel* like early game encounters."
3. "It was entirely too static... every route looked/felt the same odds wise, there was no
   creative flair to it."

The survey shows none of these were execution errors. All three are what you get when you
apply the genre-standard encounter design, which four unrelated challenge hacks converge
on independently. The previous attempt succeeded at building the wrong thing.

So this tool is not a spreadsheet with a nicer front end. It encodes a *different* design
model, measures whether a set of tables actually embodies it, and refuses to ship tables
that don't.

---

## 1. Ground truth: the Platinum encounter engine

All of this is verified against `src/overlay006/wild_encounters.c` in the decomp, not
inherited from documentation. Where a HGSS-era document disagrees, this wins.

### 1.1 Land table format

A land table is 12 slots. Fixed rates, hardcoded:

```
slot   0   1   2   3   4   5   6   7   8   9  10  11
rate  20  20  10  10  10  10   5   5   4   4   1   1
```

Each slot carries **one species and one level**. Gen 4 has no min/max range per slot —
unlike Gen 3 — which is what makes repel filtering exactly computable.

On disk: `res/field/encounters/encounters_<area>.json`, one file per area.

```json
{
  "land_rate": 30,
  "land_encounters": [ {"level": 14, "species": "SPECIES_BIDOOF"}, ... 12 entries ],
  "swarms": [ ... 2 ], "day": [ ... 2 ], "night": [ ... 2 ], "radar": [ ... 4 ],
  "ruby": [...], "sapphire": [...], "emerald": [...], "firered": [...], "leafgreen": [...]
}
```

`land_rate` controls steps-per-encounter, not the distribution. It is a separate design
knob (see 7, R9).

### 1.2 Repel — exact behaviour

```c
static BOOL RepelPreventsEncounter(const u8 wildLevel, const WildEncounters_FieldParams *p)
{
    return p->repelActive && p->firstBattlerLevel > wildLevel;
}
```

Two things follow, and both matter:

- **An encounter survives when `wildLevel >= leadLevel`.** Greater-than-or-equal, not
  strictly greater. A lead at level 14 still meets level-14 wilds.
- **A blocked roll cancels the step.** The game does not re-roll onto a surviving slot.
  So, *conditional on an encounter happening at all*, the distribution is exactly the
  surviving slot weights renormalized. Nothing is smeared.

Therefore, with lead level `L`:

```
P(slot i | encounter) = w_i / Σ{ w_j : level_j >= L }        for level_i >= L
                      = 0                                     otherwise
```

This is the entire repel model. It is simple, it is exact, and the tool must never
approximate it.

### 1.3 Slot substitution layers

Applied at encounter time on top of the base table. Base table = **morning**.

| Layer | Slots replaced | In scope? |
|---|---|---|
| Time of day (`day`, `night`) | 2, 3 | **Yes** |
| Swarm | 0, 1 | No |
| Trophy Garden | 6, 7 | No |
| Dual-slot GBA | 8, 9 | No |
| Poké Radar | separate code path | No |

Out-of-scope layers are still *read* by the tool and shown greyed, so Ian can see what
would collide if he later turns one on. They are never written.

Because day/night only touch slots 2 and 3, each of those is worth exactly 10%, and a
day/night swap moves at most 20% of a table. This is a tighter constraint than it looks:
a route cannot change character between morning and night, only accent.

### 1.4 Scope

**In:** land tables for every area, morning/day/night variants, levels, `land_rate`.

**Out of the first pass, tracked for later:** honey trees, in-game trades, gift and static
Pokémon, swarms, radar, dual-slot, Trophy Garden. Availability accounting (section 2.4)
must eventually include trades and gifts, because a line given by a trade should not also
need a wild slot. Until then the tool treats them as absent and Ian hand-adjusts. The gift
Pokémon are already catalogued in `docs/oxide/pokemon-gifts.md`, ready for that accounting.

*(v1.1)* Water and the three rods were also out of the first pass as written, but came in
with M4 for 53 areas: surf and old rod roll 60/30/5/4/1, good and super rod 40/40/15/4/1,
and a water slot carries a level range rolled uniformly, so a repel admits a fraction of a
slot. They are read, analysed and editable. The linter stays land-only because every rule
was calibrated on land tables.

---

## 2. The design model

This section is the actual content. Everything after it is plumbing.

### 2.1 The three complaints as measurable properties

| Complaint | Property | Vanilla Platinum | Challenge-hack norm | Oxide target |
|---|---|---|---|---|
| 1. Manips never pay | median uplift on a table's rarest species from the best repel tier | **5.0x**, works on 88% of tables | 1.45x, 64% | ≥3.0x, ≥80% |
| 2. Early doesn't feel early | HHI of early tables (median level ≤12) vs late (≥30) | 0.37 → 0.28 | 0.14 → 0.18 (backwards) | ≥0.35 early, ≤0.25 late |
| 3. Everything feels the same | p10-p90 spread of HHI across tables with 3+ species | 0.170-0.420 (**2.5x**) | 1.3-1.6x | ≥2.2x |
| 3. (corollary) | distinct weight signatures per table | 71 / 171 = **0.42** | 0.12-0.19 | ≥0.35 |

HHI is the Herfindahl index: Σ(share²). One species at 100% gives 1.0; twelve equal slots
give 0.083. It is the single number that says "how concentrated is this table".

*(v1.1)* Two of the targets sit beyond vanilla and are meant to. Row 1's "5.0x" is the best
uplift available to *any* species on the table (vanilla measures exactly 5.00x on 88%); the
rarest-species uplift is 3.33x on 83%, and R3's 3.0 threshold is calibrated on that, so it
is passed by 52% of vanilla tables rather than most of them. Row 2's late target of ≤0.25 is
below vanilla's 0.275; the *shape* (early above late) is what vanilla does, the bounds are
aspirational (R11 versus R11b in section 7).

That last row is the sharpest indictment of the old approach. Hardlove used **three**
templates. The genre standard uses about 25 distinct shapes. Vanilla Platinum uses 71,
and three of the four surveyed hacks share the *exact same* most common signature:
`(20,20,10,10,10,10,10,10)` — which is just the slot rates with the tail folded into the
10s. A table shape should be a decision, not a default.

### 2.2 The level ladder

This is the mechanism that makes repel manips worth doing, and it is already in the base
game. Vanilla Platinum's median level offset above each table's own minimum, by slot:

```
slot   0   1   2   3   4   5   6   7   8   9  10  11
rate  20  20  10  10  10  10   5   5   4   4   1   1
level +0  +1  +1  +1  +2  +2  +2  +2  +2  +2  +3  +3
```

**Level rises monotonically with slot rarity.** 136 of 171 vanilla tables have exactly
four distinct levels. The consequence: a repel cuts the table off at the bottom, so each
rung up discards the common head and renormalizes the remaining mass onto the rare tail.
Four rungs, four pools, each smaller and richer than the last.

Only 6% of vanilla tables put a species in the 1% slots that appears nowhere else on the
table. So the ladder is not a rare-exclusive delivery system. It is a **re-weighting**
device: it changes which of the table's own species you meet, and by how much.

Both surveyed hacks with published level data compressed the band to a median of 2 levels.
That alone flattens the ladder to two rungs and is most of why their repel uplift
collapsed to 1.45x.

**House rule for Oxide:** every table declares a ladder. Levels are assigned monotonically
non-decreasing with slot index. Default is a four-rung ladder at `+0 / +1 / +2 / +3`, and
a route archetype may override it.

The rung a species occupies is a first-class design decision, separate from its weight.
A 10% species on rung 3 is a completely different experience from a 10% species on rung 0.

### 2.3 Route archetypes

Replaces the old QUAD6 / TRI7 / PENTA7 template scheme. An archetype is a **weight
signature + a ladder + a tail policy + a stated intent**. These are fitted from measured
vanilla Platinum tables, not invented; the count next to each is how many vanilla tables
carry that exact signature.

| # | Name | Signature | HHI | Ladder | Tail | Intent |
|---|---|---|---|---|---|---|
| A1 | **Route** (40x) | 40/25/20/10/5 | 0.275 | 4 rungs | duplicates | The default Sinnoh route. One face, one sidekick, three extras. |
| A2 | **Monoculture** (27x) | 100 | 1.000 | 1 rung | none | Old Chateau. A place that is *about* one species. No manip, none needed. |
| A3 | **Sanctuary** (6x) | 80/10/10 | 0.660 | 2-3 rungs | real | One species dominates; the 10s are the reason to repel. Strong early-game feel. |
| A4 | **Duo** (3x+2x) | 65/35 or 50/50 | 0.50-0.55 | 2 rungs | none | Ravaged Path. A coin flip with a lead-level tiebreaker. |
| A5 | **Tiered** (6x) | 40/25/20/9/4/1/1 | 0.272 | 4 rungs | **real 1%** | The lottery route. Top rung is 2-3 species and contains the prize. |
| A6 | **Marsh** (4x) | 30/30/25/10/5 | 0.255 | 3 rungs | duplicates | Three co-equal faces. Feels busy without feeling flat. |
| A7 | **Spread** (2x) | 25/25/15/15/10/10 | 0.190 | 3 rungs | duplicates | Route 204 North. Genuinely varied; use sparingly. |
| A8 | **Broad** (7x) | 20/20/20/10/10/10/5/5 | 0.155 | 3-4 rungs | duplicates | Mt. Coronet. The genre's default shape. Allowed, but rationed — see R4. |
| A9 | **Dominant** (2x) | 50/20/20/10 | 0.340 | 3 rungs | none | Iron Island rooms. Clean, readable, low variance. |
| A10 | **Lottery** (new) | 60/25/10/4/1 | 0.436 | 4 rungs | **real 1%** | Designed for Oxide. The 1% is something you actually want, and the top rung is 2-3 wide. This is the archetype that pays off a dupe-out plan. |

Ian picked **"per-route, chosen by archetype"** for tail treatment, which is exactly what
the Tail column encodes. `real` means the 1% slots hold a species found nowhere else on
that table; `duplicates` means the tail repeats head species at the top rung (vanilla's
usual move, and the thing that drives re-weighting); `none` means there is no meaningful
tail because the ladder has fewer rungs.

**Archetype budget.** A game's worth of tables must hit the spread target (2.2x), so the
mix is constrained, not free. Vanilla Platinum's distribution, as a starting budget:

| HHI band | Share of tables | Archetypes |
|---|---|---|
| ≥0.55 (concentrated / single) | ~18% | A2, A3, A4 |
| 0.35-0.55 | ~14% | A9, A10 |
| 0.20-0.35 | ~50% | A1, A5, A6 |
| <0.20 (broad) | ~18% | A7, A8 |

The linter checks the realised mix against this budget, not against each table.

### 2.4 Availability, and why it is also the source of variety

Ian's call: **availability guaranteed, bought Drayano's way** — a moderate roster repeated
across many areas, rather than a huge roster placed once each.

The survey says this costs variety: Renegade Platinum repeats heavily and has a 1.6x HHI
spread. But that is not causation, and the counter-example is in the same dataset. Vanilla
Platinum repeats *harder* than Renegade Platinum does — one species appears on 79 tables,
only 26% of species are area-exclusive — and still has a 2.5x spread.

The difference is that Drayano repeats a species at a **similar weight everywhere**.
Vanilla puts the same species on a different rung of a different ladder on each table.
Starly is the 20% face of Route 201 and a 4% tail slot somewhere else.

**So the house rule is: repetition is where variety comes from, not what it costs.**

> A species may appear on many tables, but its *weight signature position* must vary.
> Concretely: for any species on 4+ tables, its shares across those tables must span at
> least a 4x ratio (e.g. 20% somewhere and ≤5% somewhere else).

This single rule reconciles the two answers. It makes availability cheap — a line only
needs one good table plus several cameo appearances — while forcing the cameos to be
genuinely different in character. It is also what generates the cross-table dupe-out
structure in 2.6, because a species that is 1% here and 25% there is precisely the thing
worth pre-catching.

**Availability accounting.** For each line on the pick-list the tool computes an
*acquisition cost*: the minimum over all tables and all repel tiers of expected encounters
to first catch, given a plausible party state. A line is "available" if that cost is under
a threshold Ian sets per tier (see R7). Guarantee is checked against this number, not
against "does it appear somewhere".

### 2.5 The concentration arc

Early game feels early through **concentration and a small cast**, not through low levels.
Vanilla early routes: 4 species, top slot 45-48%, HHI 0.37-0.41. Late routes: 5 species,
top slot 30-40%, HHI 0.24-0.28.

Every surveyed challenge hack is flat end to end, and two run backwards. Radical Red gives
early routes eleven species and late routes seven.

**House rule:** archetype selection is biased by progression band.

| Band (median table level) | Target species/table | Target top slot | Target HHI | Preferred archetypes |
|---|---|---|---|---|
| Early (≤12) | 3-5 | 40-50% | 0.35-0.50 | A1, A3, A4, A9, A10 |
| Mid (13-29) | 4-7 | 30-40% | 0.25-0.35 | A1, A5, A6, A9 |
| Late (30+) | 5-8 | 25-35% | 0.18-0.28 | A1, A5, A6, A7, A8 |

The cast grows as the game opens up. That is the arc, and it is the opposite of what the
genre does.

### 2.6 The dupes clause and the dupe-out cascade

Confirmed as a house rule for Oxide: an encounter of an already-owned species does not
count.

Two distinct numbers, and the tool shows both:

- **Conditional odds.** Given an encounter that *counts*, the chance it is species `s`:
  `P(s | s ∉ D) = W_s / Σ{ W_t : t ∉ D }` where `W` is post-repel mass and `D` is the
  owned set.
- **Throughput.** Expected encounters until something counts: `1 / (Σ{W_t : t ∉ D} / ΣW)`.

A design can be great on the first and miserable on the second. Both go on screen.

**The cascade.** This is Ian's model, and it is the feature the whole tool exists to serve:

> "If a late game encounter table has 99% rattata and 1% mewtwo, a previous table that has
> rattata as part of a repel manip is suddenly very enticing because it can guarantee you
> a later mewtwo."

So the value of a table is not only what it gives you. It is also **what it lets you
remove from a later table**. A 1% prize behind 99% junk is unreachable — unless the junk
is catchable cheaply somewhere earlier, at which point the dupes clause deletes it and the
prize goes from 1% to 100%.

This is why "guaranteed" manips are boring and 2-4 species pools are the target. Ian:
*"A manip for something that is 'guaranteed' has very binary logic... If you can manip
down to 2 pokemon or 4 pokemon, but because you have some of them duped out your odds at
the 'good' one are now much higher than normal, there is now a decision tree."*

*(v1.1, corrected)* Vanilla Platinum sits in the right place naturally, but not as narrowly
as v1.0 said. The original "only 8% of repel tiers collapse to a single species" does not
reproduce: measured on vanilla it is **24%** of rungs, with 43% of tables having at least
one singleton. The base ROM's tables measure 7%, which suggests the 8% was computed against
a working tree that already held them. The rule survives with the corrected justification:
at most one singleton rung per table (R6) passes 84% of vanilla.

---

## 3. Data model

### 3.1 Source of truth

**The decomp files are the tool's state.** `res/field/encounters/*.json` is read on start
and written on save. There is no separate database, no export step, no sync. The tool is a
view over the repo.

Consequences, all of them good:
- Every edit Ian makes lands as a git diff he can read, revert, or hand to Claude Code.
- `make rom` after saving produces a ROM with those encounters. No import pass.
- Two people (Ian in the UI, Claude Code on the CLI) edit the same bytes and git arbitrates.

**Writing rule, carried over from the species/move importer:** edit by targeted key
replacement, never by re-serialising the whole file. Whole-file rewriting was abandoned
during the species import because the decomp's JSON style is not reproducible from Python
(`[  ]` for empty arrays, inline arrays capped at 2 scalars, ASCII escaping). Untouched
text must produce no diff. Reuse `tools/oxide/jsonstyle.py`.

### 3.2 The sidecar

Design intent that has nowhere to live in the decomp format goes in one file:

`docs/oxide/encounters/design.json`

```json
{
  "areas": {
    "encounters_route_205_south": {
      "archetype": "A5",
      "band": "mid",
      "intent": "The Budew route. Real 1% tail holds the regional fossil-line stand-in.",
      "locked": ["land_encounters[10]", "land_encounters[11]"],
      "ladder": [0,1,1,1,2,2,2,2,2,2,3,3],
      "base_level": 14
    }
  },
  "budget": { "concentrated": 0.18, "mid": 0.50, "broad": 0.18, "dominant": 0.14 },
  "thresholds": { "...": "everything in section 7, editable" }
}
```

`locked` marks slots the generator may not touch — Ian's hand-placed decisions. The
generator is free to rearrange everything else.

This file is human-readable and hand-editable on purpose. It is also the thing Ian diffs
when he wants to know *why* a route looks the way it does.

### 3.3 Species universe

Read `docs/oxide/species-pick-list.csv` into a species table
with: national dex number, evolution line id, type(s), stage, and a `tier` field Ian can
set (`starter-adjacent`, `preferred`, `filler`, `gate`). Tier drives availability
thresholds and archetype eligibility. A `preferred` line is allowed to sit in a manip tier
— the old design forbade this, which is precisely why manips never paid.

---

## 4. Architecture

```
tools/oxide/encounters/
  server.py        # stdlib http.server, binds 127.0.0.1:8765, no deps
  model.py         # load/save decomp JSON + sidecar; the write-by-key-replacement path
  analysis.py      # section 6 math. Pure functions, no I/O.
  lint.py          # section 7 rules. Pure functions over analysis output.
  generate.py      # section 8. Pure functions + a search loop.
  cli.py           # headless entry points for Claude Code
  ui/index.html    # single page, vanilla JS, no build step, no CDN
```

**Why a local server rather than an artifact.** Established in
`claude/hardlove-editor-tool.md`: a sandboxed browser artifact cannot hold or write repo
files, the File System Access API needs a secure non-sandboxed context, and the previous
tool had to route edits through a JSON patch plus an `apply_patch.py` step. Running in WSL
next to the repo removes all of that. `python3 -m tools.oxide.encounters.server` and open
`localhost:8765`.

**No dependencies.** Python stdlib and vanilla JS. This tool must still start in two
years. No npm, no pip install, no CDN script tags.

**Two front doors, one engine.** The UI and the CLI both call `analysis.py` and `lint.py`.
Any number the UI shows, Claude Code can get as JSON:

```
python3 -m tools.oxide.encounters.cli report  [--area X] [--json]
python3 -m tools.oxide.encounters.cli lint    [--fail-on error]
python3 -m tools.oxide.encounters.cli plan    --area X --species Y
python3 -m tools.oxide.encounters.cli generate --band early --dry-run
```

`lint --fail-on error` is what runs before a commit.

---

## 5. The UI

One page, three columns. No modals, no wizards, no save button that can be forgotten —
edits write on blur and the header shows the git status of the encounter files.

**Left — area list.** Every area, with its archetype badge, band, species count, HHI, and
a red dot if it fails lint. Sortable by any of those, filterable by band, archetype, or
"contains species X". Sorting by HHI is how Ian sees the spread at a glance.

**Centre — the table editor.** Twelve rows, one per slot, showing index, rate, species
(typeahead over the pick-list), level, and rung. Below it, three things:

- The **merged view**: species collapsed with total share, sorted descending. This is the
  number Ian thinks in, and the one every published hack document prints.
- The **ladder view**: a small stacked bar per rung showing the surviving pool and its
  renormalized shares. This is the repel structure, visible.
- Morning / day / night tabs. Day and night only expose slots 2-3, greyed elsewhere, with
  the base values shown behind them.

Edits are slot-level. Editing the merged view is not supported — it hides the ladder, and
the ladder is the point.

**Right — live analysis.** Everything from section 6 for the current table, recomputed on
every keystroke:

- base odds, per species
- a row per repel rung: lead level, surviving pool, each species' odds, pool size
- the **uplift number** for the table's rarest species, in the same units as section 2.1,
  coloured against the 3.0x target
- dupes panel: a checkbox per species on the table; ticking simulates owning it and the
  odds and throughput numbers update
- **Dupe-Out Planner** (6.4) — the feature that implements 2.6
- lint results for this table, each rule naming itself

**Header.** Game-wide metrics: HHI spread, distinct signatures, archetype budget vs
realised, early/mid/late arc, count of lines failing availability. These are the numbers
that say whether the *set* is good, as opposed to any one table, and they need to be
visible while editing a single table — otherwise every local fix drifts the global shape.

---

## 6. The analysis engine

Pure functions. No I/O, no globals. Every one of these is independently testable, and
section 11 says which ones ship with tests.

### 6.1 Base odds

```
base(table) -> {species: share}     share = Σ rates of slots holding that species
```

### 6.2 Repel-conditional odds

```
rungs(table) -> [lead_level]        sorted distinct slot levels
pool(table, L) -> {species: share}  renormalized over slots with level >= L
```

Per 1.2, `>=`, and renormalization is exact because a blocked roll cancels the step.
Collapse rungs that yield an identical pool — the UI should show four rungs when there are
four *distinct* outcomes, not four levels that produce three pools.

### 6.3 Dupes-conditional odds

```
conditional(pool, owned) -> {species: share}   restricted to species not in owned, renormalized
throughput(pool, owned)  -> float              expected encounters per counting encounter
```

### 6.4 The Dupe-Out Planner

Input: a target area `T` and a target species `Y` on it.

For every subset-of-interest `D` of the other species on `T`, and every rung `L`:

1. compute `P(Y | L, D)`
2. for each `Z ∈ D`, find its cheapest acquisition: minimise expected encounters over all
   areas and rungs, restricted to areas reachable before `T` in progression order
3. total cost = Σ acquisition costs + expected encounters at `T` under `(L, D)`

Report the Pareto front of (total cost, `P(Y)`), and render the best few in plain language:

> **Route 214, target Gible (4%).**
> Repel with a level-32 lead → pool is Gible / Hippopotas / Graveler, Gible at 11%.
> Pre-catch Hippopotas (Route 214 itself, 25%, ~4 encounters) and Graveler
> (Mt. Coronet 3F, level-30 manip, 100%, ~2 encounters) → **Gible at 100%.**
> Total ≈ 6 encounters, versus ≈ 25 unplanned.

Search space is small — a table has at most 12 species, and only rungs where `Y` survives
are worth considering — so exhaustive enumeration is fine. Do not get clever.

This is the feature that answers complaint 1. If the planner cannot find a route from a
bad baseline to a good outcome on a decent fraction of tables, the tables are wrong, not
the planner.

### 6.5 Per-table metrics

`n_species`, `top_share`, `min_share`, `HHI`, `rung_count`, `pool sizes per rung`,
`uplift_on_rarest`, `has_real_tail`, `band`, `archetype`, `archetype_fit` (distance from
the declared signature).

### 6.6 Per-game metrics

`HHI p10/median/p90` over tables with 3+ species, and the p90/p10 ratio; count of distinct
weight signatures and signatures-per-table; realised archetype budget; early/mid/late
medians of species count, top share and HHI; per-species area count and share range;
per-line acquisition cost; count of lines above threshold.

---

## 7. The linter

Every threshold lives in `design.json` and is Ian's to move. Severity: **error** blocks a
commit, **warn** shows in the UI and in `report`.

*(v1.1)* Every rule is also tagged **descriptive** or **aspirational**, and the tag lives
in `lint.py` beside the rule. A descriptive threshold states something vanilla already
does, so criterion 6 applies to it: if vanilla fails it, the threshold is wrong. An
aspirational threshold is set beyond vanilla on purpose, so vanilla is expected to fail it,
and a vanilla failure is not a bug. Do not "fix" a rule vanilla fails until checking which
kind it is. The vanilla pass rates below are from M3.

**Per-table**

- **R1 (error, authored tables only) — Ladder monotonicity.** Slot levels are
  non-decreasing with slot index. A house rule for tables Oxide writes: the generator
  assigns levels this way and a hand edit that breaks it is almost always a mistake.
  *(v1.1)* **Not a description of vanilla and never checked against it**: only 20 of 171
  vanilla tables are monotonic by slot index (Route 201 puts its 1% slots at the table's
  minimum level). The v1.0 text calling this "the single highest-leverage rule" was
  describing the ladder as a correlation, which is R1b.
- **R1b (warn, descriptive) — Ladder correlation.** Rarity-vs-level Spearman ≥ 0.5.
  Vanilla medians 0.68 and 71% of tables pass. This is the form that can be pointed at
  both corpora.
- **R2 (warn, descriptive) — Rung count.** 3-4 distinct rungs, unless the archetype declares
  fewer (A2, A4). Vanilla 81%.
- **R3 (warn, aspirational) — Repel pays.** `uplift_on_rarest ≥ 3.0`. Vanilla medians 3.33x
  on the rarest species and passes on 52% of tables; the 5.0x in v1.0 was `best_uplift`,
  the best manip available to any species, which vanilla hits on 88%. Both statistics are
  reported. The threshold is kept at 3.0 as a target above vanilla.
- **R4 (warn) — Archetype fit.** Realised signature within tolerance of the declared one.
  Only runs on tables with a declared archetype.
- **R5 (warn, aspirational) — Band fit.** Species count, top share and HHI inside the 2.5
  band targets. Vanilla passes 11-32% depending on band; the bands describe what Oxide
  wants, not what vanilla does.
- **R6 (warn, descriptive) — Not too binary.** At most one rung collapses to a single
  species, and the top rung holds 2-4. *(v1.1)* Vanilla: 24% of rungs are singletons (not
  8%), and 84% of tables pass the rule as written.
- **R7 (error) — Day/night legality.** Day and night differ from base only at slots 2-3.
  Enforced structurally in `model.py` as well: a write outside those slots is refused.

**Per-game**

- **R8 (error, descriptive) — Spread.** HHI p90/p10 over 3+ species tables ≥ 2.2. Vanilla
  2.48x, challenge hacks 1.3-1.6x, the project's current tables 2.14x. *This is the rule
  that prevents complaint 3, and it cannot be satisfied by editing one table — it forces
  the archetype mix.*
- **R9 (warn, descriptive) — Signature diversity.** Distinct weight signatures per table
  ≥ 0.35. Vanilla 0.42; the genre 0.12-0.19; Hardlove had three templates for the whole
  game; the current tables 0.26.
- **R10 (warn) — Archetype budget.** Realised mix within 5 points of 2.3's budget. Only
  runs once archetypes are assigned.
- **R11 (warn, descriptive) — Arc shape.** Median HHI strictly decreasing across the three
  bands. Vanilla 0.373 > 0.325 > 0.275; the current tables run backwards.
- **R11b (warn, aspirational) — Arc bounds.** Early ≥ 0.35, late ≤ 0.25. *(v1.1)* Split
  out of R11 because vanilla's late band is 0.275 and cannot pass ≤ 0.25.
- **R12 (error) — Availability.** Every line on the pick-list has an acquisition cost
  below its tier's threshold. This is Ian's guarantee, in its enforceable form. Reports
  itself as *skipped*, not passed, until the pick-list has a `tier` column.
- **R13 (warn, aspirational) — Repetition varies.** Any species on 4+ tables spans ≥ 4x
  between its largest and smallest share. *This is the rule that makes Drayano-style
  availability generate variety instead of consuming it.* *(v1.1)* Vanilla's median span
  is 2.5x and only 37% of repeated species reach 4x, so this asks for about double what
  vanilla does. Kept at 4x as a deliberate choice; lower it if authored tables cannot
  reach it.
- **R14 (warn, descriptive) — Encounter rate variety.** `land_rate` is not the same value
  on more than half of the tables. Free texture, and the old rewrite never touched it.
  Vanilla's commonest value covers 37%.

R8, R12 and R13 are the three that carry the design. The rest are hygiene. A rule that
cannot run (no tiers, no archetypes, bands missing) must emit a *skip* finding rather than
pass silently; a quiet skip is indistinguishable from a pass in the output.

---

## 8. Generation and automation

Ian's ask: *"help me figure out what we can do to improve the logic of implementing /
training on encounter data to automate some of the easier parts of this design."*

### 8.1 Not machine learning

The honest answer first. The training corpus is 171 vanilla tables plus a few hundred from
hacks whose design is the thing being rejected. That is far too small to learn from, and
learning from it would reproduce the genre average — which is exactly the failure mode.

What "training on encounter data" should actually mean here:

1. **Fit the archetype library from measured tables** (done — section 2.3 comes from the
   vanilla Platinum signature census, not from taste).
2. **Turn the design into a scoring function** (done — section 7 is the scorer).
3. **Search the placement space against that score** (below).

That is a constraint-satisfaction problem with a measured objective. It is fully
automatable, it is deterministic, and every decision it makes is explainable.

### 8.2 The pipeline

**Step 1 — Assign archetypes and bands.** Input: the area list in progression order, with
each area's intended level. Assign a band from level, then draw archetypes to satisfy the
2.3 budget and the 2.5 band preferences. Deterministic given a seed. *Automatable.*

**Step 2 — Place species.** A constrained assignment. Hard constraints: every line meets
R12; no line appears before its intended progression point; type/theme tags match the
area's tags (Ian's flavour input); `locked` slots are immovable. Soft objective: R13's
share-range spread, thematic coherence, evolution lines appearing near each other.
Greedy seeding plus local search (swap two species between tables, keep if score
improves). *Automatable.*

**Step 3 — Assign levels and rungs.** Given a table's species and the archetype's ladder,
walk the slots and assign levels monotonically from `base_level`. Then hill-climb: try
moving each species between rungs, score with R3 and R6, keep improvements. This step is
where the repel structure is actually created, and it is cheap because the search space
is tiny. *Automatable, and the highest value per line of code in the whole pipeline.*

**Step 4 — Lint, repair, report.** Run section 7. For each failure, attempt the scripted
repair (see below). Report what it changed and what it could not fix. *Automatable.*

**Step 5 — Ian reviews in the UI.** He locks what he likes, rewrites what he doesn't,
writes `intent` strings, and re-runs from step 2 with the locks honoured. *Not automatable
and should not be.* The generator's job is to produce a defensible draft fast, not to have
opinions about whether Gible belongs on Route 214.

### 8.3 Scripted repairs

Each of these is a small deterministic edit the tool may apply when a rule fails:

| Failure | Repair |
|---|---|
| R1 monotonicity | Sort slot levels ascending, keeping species attached |
| R2 rung count | Split the largest rung by pushing its rarest slot up one level |
| R3 uplift too low | Move the rarest species up one rung; re-check |
| R6 too binary | Add a duplicate of a head species to the top rung |
| R11 arc | Swap an early broad table's archetype for a concentrated one, re-place |
| R13 repetition | Demote one appearance of an over-uniform species to a tail slot elsewhere |

Every repair is logged to `docs/oxide/encounters/repairs.log` with the rule, the area, and
the before/after. Repairs are proposals in the UI and applied automatically only under
`generate --repair`.

### 8.4 The lesson that governs all of this

From `claude/hardlove-encounter-slot-rates.md`: *"Documentation matched the model; the game
did not. Measurement beats any amount of internal consistency in a document."*

So: the generator never reports success from its own model. It reports success from
`lint`, which reads the files on disk. And section 11's acceptance test re-reads the built
ROM's NARC rather than the source JSON, because that is the only thing the game runs.

---

## 9. Ian's workflow

**Normal edit.** Start the server, open the area, change a slot, watch the right column.
Save is automatic. `git diff` shows exactly what moved. When happy, `make rom`.

**Designing a route from scratch.** Pick an archetype, write the `intent` line first, let
the tool lay out the ladder, then drop species in. The intent line is not decoration — it
is what Ian reads in six months when he wonders why Route 210 looks like that.

**Bulk pass.** `cli generate --band early --dry-run` writes a proposed diff without
touching files. Review, then re-run without `--dry-run`.

**Before a commit.** `cli lint --fail-on error`. Wire it as a pre-commit hook once the
tables stabilise.

**Handing work to Claude Code.** Ian describes the change in prose; Claude Code makes it
through `cli`, runs `lint`, and reports the deltas on the section 6.6 metrics. It never
edits the JSON by hand — the tool is the only writer, so the style-preservation guarantee
holds.

---

## 10. Out of scope, tracked

- **Honey trees, in-game trades, gift and static Pokémon.** Must eventually feed R12's
  availability accounting: a line handed over by a trade should not also consume a wild
  slot. Until then R12 over-reports and Ian hand-waives.
- Rock Smash tables. Same engine, same math, different rate array; the analysis layer is
  rate-array-agnostic so adding them is a config change. *(v1.1)* Surf and the three rods
  are already in (section 1.4); lint for water tables is not, pending calibration.
- Swarms, Poké Radar, dual-slot, Trophy Garden. Read and displayed, never written.
- Shiny/hue-shift interactions from the base ROM. Orthogonal.

---

## 11. Acceptance criteria

The tool is done when:

1. It loads all 185 encounter files and round-trips every one of them with a **zero-byte
   git diff** when nothing is edited. This is the first test to write and the one most
   likely to fail.
2. `analysis.pool()` matches a brute-force simulation of `RepelPreventsEncounter` over
   10⁶ trials on 20 randomly chosen tables, within Monte-Carlo error. The repel model is
   the tool's core claim; it gets verified against the actual comparison, not against a
   restatement of it.
3. Running `report` against **unmodified vanilla Platinum** (`--ref main`; the working
   tree holds the base ROM's tables) reproduces the survey's numbers: median HHI 0.275,
   spread 0.170-0.420, 71 distinct signatures, best uplift 5.0x working on 88% (rarest
   species 3.33x on 83%), ladder `+0/+1/+1/+1/+2/+2/+2/+2/+2/+2/+3/+3`. If the tool
   disagrees with the survey, one of them is wrong and it must be found before any table
   is designed. *(v1.1)* Met by M2, which is how the 8% and 5.0x definitions were corrected.
4. The UI renders a table, accepts an edit, and the change appears in `git diff` at the
   right key with no other key touched. *(v1.1)* Met by M4.
5. The Dupe-Out Planner produces a correct multi-step plan for at least one hand-verified
   case.
6. `lint --ref main` on vanilla Platinum passes every **descriptive** rule: R1b, R2, R6,
   R8, R9, R11 and R14 — because vanilla *is* the target for those. If vanilla fails one,
   the rule's threshold is wrong. *(v1.1)* R1 is not on this list (see section 7) and the
   aspirational rules R3, R5, R11b and R13 are expected to fail on vanilla. Met by M3.

Criterion 6 is the sanity check on this entire document. The design model claims vanilla
Platinum got something right that the genre lost. If the linter that encodes the model
can't pass the thing it was derived from, the model is miscalibrated.

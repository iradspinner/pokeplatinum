# Encounter design survey: what challenge hacks actually do

Measured 2026-09-20 for Platinum Oxide. Seven datasets, land/grass tables only, read
from decomp sources or the hack's own published documentation. Scripts:
`unify.py`, `unify2.py`, `repel.py`, `layout.py`.

## Sources

| Dataset | Tables | Source |
|---|---|---|
| Platinum (vanilla) | 171 | `pret/pokeplatinum` `res/field/encounters/*.json` |
| FireRed (vanilla) | 226 | `pret/pokefirered` `src/data/wild_encounters.json` |
| Emerald (vanilla) | 95 | `pret/pokeemerald` |
| Renegade Platinum 1.3 | 246 | Drayano's `Wild Pokemon.txt`, via `zhenga8533/renegade-platinum-wiki` |
| Radical Red 4.1 | 144 | `idoggiebites-oss/radical-red-tracker` `src/data/encounters.json` |
| Inclement Emerald | 122 | `kleeenexfeu/inclementemerald` `src/data/wild_encounters.json` |
| Elite Redux | 124 | `Elite-Redux/eliteredux` |

Gen 3 and Gen 4 land tables use identical slot rates `[20,20,10,10,10,10,5,5,4,4,1,1]`,
so all seven are directly comparable. Renegade Platinum and Radical Red are
documentation-derived: merged percentages per species, no per-slot levels, so they
carry shape metrics but not repel metrics.

## Headline table

| | species/table | top slot | rarest slot | HHI median | HHI p10-p90 (3+ sp) | early → late HHI |
|---|---|---|---|---|---|---|
| Platinum vanilla | 5 | 40% | 5% | 0.275 | 0.170-0.420 | 0.37 → 0.28 |
| FireRed vanilla | 5 | 40% | 5% | 0.280 | 0.160-0.415 | 0.41 → 0.24 |
| Emerald vanilla | 3 | 55% | 10% | 0.455 | 0.209-0.460 | 0.36 → 0.46 |
| Renegade Platinum | 7 | 20% | 10% | 0.160 | 0.135-0.220 | 0.20 → 0.17 |
| Elite Redux | 7 | 20% | 10% | 0.160 | 0.135-0.180 | 0.14 → 0.18 |
| Inclement Emerald | 7 | 20% | 10% | 0.160 | 0.140-0.200 | 0.16 → 0.18 |
| Radical Red 4.1 | 8 | 20% | 2% | 0.157 | 0.129-0.185 | 0.13 → 0.16 |

HHI = sum of squared shares; 1.0 is one species at 100%, 0.083 is twelve equal slots.
"early/late" bins tables by median encounter level (<=12 and 30+).

## Finding 1 — the genre has one table shape, and it is the one you disliked

Four unrelated hacks, three different base games, two different authors' philosophies,
and they land on the same number: **6-8 species, top slot 20%, HHI 0.157-0.160**. That
is not convergent evolution, it is the same arithmetic. Twelve slots, "every line should
be gettable", dupes-clause players — you get a flat table every time.

Hardlove's encounter rewrite was not a failed execution of a good design. It executed the
genre standard correctly, and the genre standard is what produces "every route looks and
feels the same odds-wise".

## Finding 2 — vanilla has twice the route-to-route variety of any challenge hack

Comparing the p10-p90 spread of HHI across tables with 3+ species:

- Platinum vanilla: 0.170-0.420, a **2.5x** range
- FireRed vanilla: 0.160-0.415, **2.6x**
- Renegade Platinum: 0.135-0.220, **1.6x**
- Radical Red: 0.129-0.185, **1.4x**
- Elite Redux: 0.135-0.180, **1.3x**

Vanilla routes disagree with each other about what a route is. Challenge-hack routes do
not. The lever for complaint 3 is not "flatter" or "steeper" on average — every hack has
the same average. It is **the width of the distribution of shapes**. That is a
first-class design target the tool should measure and enforce, not a side effect.

## Finding 3 — early game feels early through concentration, not level

Vanilla early routes (median level <=12): 4 species, top slot 45-48%, HHI 0.37-0.41.
Vanilla late routes: 5 species, top slot 30-40%, HHI 0.24-0.28. FireRed's arc is the
clearest: 0.41 → 0.24.

Every challenge hack is flat end to end. Elite Redux and Inclement Emerald actually run
*backwards* (0.14 → 0.18). Radical Red gives early routes **more** species than late ones
(11 vs 7).

"Early game encounters did not feel like early game encounters" has a measurable cause:
early tables in a challenge hack have 7-11 species at 20% each, where the thing that
makes Route 201 feel like Route 201 is 4 species with one of them at half the table.

## Finding 4 — flattening the table destroys repel manipulation

This is the one that matters most. For each table, take its rarest species and ask: what
is the best probability of that species reachable through a repel, versus its base rate?

| | tables with a working repel | 2x or better | median uplift on rarest | rarest species survives the filter |
|---|---|---|---|---|
| **Platinum vanilla** | **88%** | **69%** | **5.0x** | **83%** |
| Emerald vanilla | 70% | 51% | 2.5x | 82% |
| FireRed vanilla | 78% | 46% | 1.8x | 63% |
| Elite Redux | 64% | 42% | 1.45x | 76% |
| Inclement Emerald | 64% | 43% | 1.45x | 73% |

**Vanilla Platinum has the best repel structure of anything measured.** Five times the
odds on the table's rarest species, working on 88% of tables. The challenge hacks cut
that to 1.45x, which is inside the noise of "just keep walking" — exactly your
"there was effectively never a reason to manip".

The mechanism is visible in vanilla Platinum's slot layout. Median level offset above the
table's own minimum, by slot:

| slot | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rate | 20 | 20 | 10 | 10 | 10 | 10 | 5 | 5 | 4 | 4 | 1 | 1 |
| level | +0 | +1 | +1 | +1 | +2 | +2 | +2 | +2 | +2 | +2 | +3 | +3 |

**Level rises monotonically with slot rarity.** 136 of 171 tables have exactly four
distinct levels. A repel at the lead's level cuts the table off at the bottom, so each
rung up the ladder discards the common head and renormalizes onto the rare tail. Four
rungs, four pools, each smaller and richer than the last. That is the decision tree.

Only 6% of vanilla tables put a species in the 1% slots that appears nowhere else on the
table — so the ladder is not about rare exclusives, it is about *re-weighting* which of
the table's own species you meet.

Challenge hacks break this two ways: they compress the level band (Radical Red and
Renegade Platinum both sit at a median band of **2 levels**, vanilla Platinum is 3 with a
clean 4-rung ladder), and they flatten the weights so re-weighting gains little.

## Finding 5 — the tail is a live design fork

Fraction of tables with no slot below 5%:

- Renegade Platinum: **100%** (Drayano folds all of 5/5/4/4/1/1 into duplicates of head species)
- Elite Redux, Inclement Emerald, Platinum vanilla: 94%
- FireRed vanilla: 89%
- **Radical Red: 13%** — median rarest slot 2%

Radical Red is the only hack in the set that preserves a genuine rare tail. It is
therefore the only one whose tables can produce the structure you described: "99% rattata
and 1% mewtwo", where an earlier table containing rattata becomes valuable because it
lets you dupe rattata out.

## Finding 6 — availability is bought two different ways

Percentage of species appearing in exactly one area:

- FireRed vanilla 23%, Platinum vanilla 26%, Emerald vanilla 46%
- Renegade Platinum 50% (max 17 areas for one species)
- Radical Red 68% (max **7** areas)
- Elite Redux 65%, Inclement Emerald 69% (max 30)

Two strategies. Drayano keeps a moderate roster and **repeats species across many areas**.
Radical Red and the Emerald-expansion hacks ship a **huge roster placed once each**
(385-566 species). Both deliver "everything is obtainable"; they produce very different
games.

## What this implies for the tool

1. Route-to-route HHI spread is a design target with a number attached. Vanilla is 2.5x;
   challenge hacks are 1.3-1.6x. The linter should fail a set of tables whose spread is
   under about 2x.
2. Early-game concentration is a design target: early tables want 3-5 species and a top
   slot near 45%, not 7 at 20%.
3. The repel ladder is a *structural* property the tool can generate and verify: assign
   levels monotonically with slot rarity, aim for four distinct rungs, and report the
   uplift-on-rarest number per table. Target vanilla Platinum's 5x, not the genre's 1.45x.
4. The dupes clause multiplies into the ladder: effective odds are slot weight over
   *unowned* mass in the surviving pool, so the tool must show odds conditioned on both
   the lead level and the dex state.

## Open, for Ian

- Availability guarantee vs per-route character: which is primary, and if availability,
  bought Drayano's way (repeat species across areas) or Radical Red's way (big roster,
  placed once)?
- Keep a genuine 1-2% tail (Radical Red) or fold the tail into duplicates (everyone else)?

## Noted for later

Honey trees, in-game trades and gift Pokemon are out of scope for the first pass of the
tool but need handling at some point.

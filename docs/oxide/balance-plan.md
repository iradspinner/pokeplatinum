# Balance plan: scoping (draft, 2026-09-22)

This is the balance track's status home. Ian put this session in charge of
balance on 2026-09-22, once element 4 had put most moves and species in the
tree. It is a scoping draft: what "balanced" means for Oxide, how it gets
measured, what data exists, and the order of work. The questions at the end
are Ian's to answer before any tooling is built.

## The target

Ian's scale puts FireRed at 1, vanilla Platinum at 3, and Platinum Kaizo, Run
& Bun and Null at 10. Oxide aims for 6: a Drayano hack made very slightly
easier.

A number on that scale is a feeling, and the plan turns it into something
measurable by scoring each reference hack the same way. Then 6 is wherever
the scores put a hack Ian calls a 6. The nearest anchor is **Renegade
Platinum**, Drayano's Platinum hack. It plays the same map with the same
bosses in the same order, so Oxide's Roark can be set beside Renegade's Roark
and Kaizo's Roark fight by fight, with no alignment guesswork.

Oxide's rules make it harder than its trainer rosters show. It has hard level
caps, no bag items in trainer battles (Phase 3), no EVs from battling, and
nuzlocke capture rules. Renegade Platinum has none of these by default. So an
Oxide fight built to Renegade's roster would play harder than Renegade's
does. The measure therefore has to score the player's side as well as the
trainer's, not just compare parties.

A first look shows the gap is real. Here is Roark in four versions of the
same game, read from each hack's data:

| Version | Party | Levels | IVs | Held items | Natures |
|---|---|---|---|---|---|
| Vanilla Platinum | 3 | 12 to 14 | low | none | rolled |
| Oxide now (the base ROM's) | 4 | 15 to 16 | about 27 to 30 | all four | rolled |
| Renegade Platinum | 6 | 15 to 16 | 29 to 30 | all six | chosen |
| Platinum Kaizo | 6 | 13 to 16 | 30 | all six, Focus Sash included | chosen |

Oxide's Roark sits between vanilla and Renegade on structure. His moves are
weaker than either hack's: Headbutt, Leer and Constrict, where Renegade gives
coverage (Fire and Thunder Punch, Zen Headbutt) and Kaizo gives Head Smash and
Earth Power. Whether that nets out to a 6 once the rules are counted is what
this plan is for.

## What gets measured

Every metric is computed the same way for every hack, from that hack's own
data, per boss fight. The bosses are the gym leaders, rival fights, Galactic
admins and bosses, and the Elite Four and Champion. Filler trainers get the
same metrics, summed per split and weighted lower. In a nuzlocke, though, a
filler trainer can still end a run, so the worst filler fight in each split is
reported on its own.

The first group of metrics is structural, cheap, and carries across every
game:

- party size;
- the ace's level against the split's cap, and against the previous boss;
- IVs and EVs;
- whether natures are chosen;
- the share of the party holding an item, and which items;
- the share that is fully evolved;
- base stat totals as a percentile of the species the player can own by then;
- the AI flags;
- whether the fight is a double battle;
- a move-quality count: setup, hazards, priority, speed control, recovery,
  and the number of types the party hits super effectively.

The second group measures pressure, which is the part that decides how hard a
fight plays. The damage calculator already runs on Oxide's data (encounter
tool M8 D5), and the same engine runs on each reference hack's data. It
measures a boss against the **player's pool**: every species obtainable by
that split, at the cap, with average IVs and a neutral nature. For each boss
Pokemon it reports:

- the share of the pool it knocks out in one or two hits while moving first;
- the share of the pool that does the same to it.

Rolled up, the first reads as "how much of what you could bring does this
fight threaten", and the second as "how many answers you have".

The yardstick is shared. Every hack's bosses are scored against **Oxide's**
player pool at the matching split, so the question each score answers is:
"if this fight were in Oxide, how hard would it be?" That keeps a trainer's
difficulty separate from differences in each hack's wild encounters, which is
what tuning needs. Where a hack's own availability data exists, a second
score against its own pool shows how the whole game felt.

Rules become modifiers on top of the scores: whether caps are hard, whether
items are allowed in battle, and whether battling grants EVs. Oxide's rules
are fixed, so the modifiers mostly matter for calibrating against the
references.

## Reference data

The calculator Oxide vendored (hzla's `Dynamic-Calc-Decomps`, MIT) has a
`backups/` folder that was left behind at vendoring. It holds each supported
hack's species, moves and full trainer sets: level, IVs, nature, item,
ability, moves, AI flags and location. It covers almost every hack in the
reference list:

| File | Hack |
|---|---|
| `pt.js` | vanilla Platinum |
| `rp.js` | Renegade Platinum (Drayano) |
| `pkv5h.js`, `pk.js` | Platinum Kaizo (current and v4) |
| `platredux.js`, `platreduxhc.js` | Platinum Redux, normal and hardcore |
| `sgss.js` | Sacred Gold and Storm Silver (Drayano) |
| `bb2redux1-4.js`, `bb.js`, `vw.js` | Blaze Black 2 Redux and Blaze Black / Volt White (Drayano) |
| `hardlove.js` | Hardlove Gold |
| `null12.js`, `null.js` | Pokemon Null 1.2 and 1.1 |
| `hgss.js` | vanilla HeartGold and SoulSilver |

Three of them are already read and parsed as plain JSON: `pt`, `rp` and
`pkv5h` (1,873, 2,823 and 3,077 trainer sets). The table above came from
those. **Run & Bun is missing**; hzla's separate `Dynamic-Calc` repository or
Run & Bun's own documentation is the likely source. FireRed has no file there.
It is the scale's floor and needs no data, since nothing in Oxide will be
tuned towards it.

The files are 1 to 9 MB each and change upstream. The plan is to fetch them
by pinned commit and SHA-256 into a folder outside the repo, the way the base
ROM and donor ROM are kept, and never to run them: they are parsed as data.

Hacks built on other games (Hardlove, Null, Run & Bun, the Unova hacks) do
not share Platinum's bosses. They line up by milestone instead: badge number,
then rivals and villain bosses by the badge they fall between, then the Elite
Four and Champion. Their scores are read against their own cap curve.

## Calibration

The scale is Ian's, so calibration is his too. Once every reference is
scored, Ian rates the ones he has played on the same 1 to 10 scale. The
composite score is then weighted so the references land where he puts them.
Vanilla Platinum at 3 and Kaizo, Null and Run & Bun at 10 are the ends;
Renegade, Sacred Gold, Blaze Black 2 Redux, Platinum Redux and Hardlove fill
the middle. "6" is then a band of scores per milestone, not a feeling.

The difficulty curve through the game is a design choice, not a measurement:
flat, rising, or with deliberate spikes at chosen fights. Ian decides the
shape. The plan's output is where each Oxide fight sits against that band.

## Tooling

A new tool, `tools/oxide/balance/`, is built in the same way as the encounter
tool:

- a data layer that reads Oxide's trainers from `res/trainers/` and each
  reference file into one schema;
- a metrics engine;
- a report per split, with each boss's metrics beside the same boss in the
  references.

Damage comes from the vendored calculator's own engine, run headless in Node
from the vendored copy, so the tool and the calculator Ian uses give the same
numbers. The one in-game damage roll already waiting on Ian (encounter build
plan, D5) checks both. The player pool per split comes from the encounter
tool's availability plan, which already says where every line lives and in
which split. Each milestone has tests, as the encounter tool's do, and a
count that anyone can rerun.

The tool does not simulate the AI choosing moves. Platinum's AI is not
Showdown's, and element 6 has documented how it actually picks. So the
pressure scores assume the boss's best move, which is a ceiling, and the
report says so. Ian's playtests remain the final gate. The scores are there
to aim the changes and to catch outliers, and to recalibrate when Ian's feel
disagrees with them.

## Order of work

1. **B0.** Ian's answers to the questions below, and the reference files
   fetched and pinned.
2. **B1, data layer.** Oxide and every reference in one schema. The check:
   trainer and set counts match each source, and a sample of fights matches
   the calculator's own view of them.
3. **B2, structural metrics** for every reference and for Oxide as it stands.
   The check: vanilla, Renegade and Kaizo come out in that order on almost
   every metric.
4. **B3, pressure metrics** against Oxide's player pool. The check: damage
   agrees with the calculator's page and with the in-game roll.
5. **B4, calibration** to Ian's ratings, and the target band per milestone.
6. **B5, the audit.** Where every Oxide fight sits today, with the base ROM's
   trainers and the new species and moves the player can now own, listing
   every fight outside the band.

After the audit, the balance work feeds the Phase 5 passes already in the
tracker, in their existing order:

1. the level-cap split design, which must come before the trainer pass;
2. the TM pass;
3. the ability pass;
4. the trainer pass, bosses first and filler after.

Each change is re-scored as it lands, so a pass cannot push a fight out of
the band without the report showing it. Trainers can now be given a chosen
nature (encounter M8), which removes the old trade-off between a nature and
IVs. One open defect has to be fixed before the trainer pass uses the field:
the packer accepts `NATURE_COUNT` and hangs the game (encounter build plan,
QA findings).

## Questions for Ian

1. Is 6/10 judged for a nuzlocke under Oxide's rules (hard caps, no bag items
   in trainer battles)? The plan assumes yes, which is why the player's side
   is scored.
2. What shape should the curve take: flat at 6, rising towards the League,
   or with chosen spikes? Which fights, if any, should stand out?
3. How would you rate the references you have played (Renegade Platinum,
   Sacred Gold, Blaze Black 2 Redux, Platinum Redux, Hardlove Gold, and
   whichever Null you mean) on the same scale? Each rating is one more
   calibration point.
4. Where should Run & Bun's data come from, if you have a copy of its trainer
   documentation?
5. Maylene's cap: the Level Caps sheet says 39, and the encounter track
   designed to 38. Which is right?
6. Should balance cover the player's side too (species stats, abilities,
   learnsets, TMs), or only the opposition? The tracker's TM and ability
   passes suggest both.

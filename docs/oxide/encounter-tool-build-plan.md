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
PYTHONPATH=. python3 -m tools.oxide.encounters.cli lint              # errors: R12's 27 scripted lines only
PYTHONPATH=. python3 -m tools.oxide.encounters.test_m4     # expect 51/51
PYTHONPATH=. python3 -m tools.oxide.encounters.test_m5     # expect 15/15
PYTHONPATH=. python3 -m tools.oxide.encounters.cli plan encounters_route_214 growlithe
PYTHONPATH=. python3 -m tools.oxide.encounters.test_m6     # expect 19/19
PYTHONPATH=. python3 -m tools.oxide.encounters.test_m8     # expect 82/82, the dex, moves, calculator and trainer sets
PYTHONPATH=. python3 -m tools.oxide.encounters.test_step0  # expect 35/35
PYTHONPATH=. python3 -m tools.oxide.encounters.test_step1  # expect 21/21
PYTHONPATH=. python3 -m tools.oxide.encounters.test_step2  # expect 18/18
PYTHONPATH=. python3 -m tools.oxide.encounters.test_step3  # expect 28/28
PYTHONPATH=. python3 -m tools.oxide.encounters.test_step5  # expect 16/16
PYTHONPATH=. python3 -m tools.oxide.encounters.calc_export # what the calculator cannot model
PYTHONPATH=. python3 -m tools.oxide.encounters.cli generate --band early --dry-run
python3 tools/oxide/verify_narcs.py --built build/pokeplatinum.us.nds --source   # M7, after make rom
PYTHONPATH=. python3 -m tools.oxide.encounters.server      # the UI, localhost:8765 (--port for a second checkout)
```

The `--source` line is the one that closes the loop: it needs a built ROM and no
reference ROM, and it must read "all 184 tables match their source JSON". It is the
only check here that looks at what the game actually runs.

The `plan` line is the whole design in one command: it should take Growlithe from
3% to 100% by naming five earlier routes to catch on first.

The two reports are the heart of it. The first is vanilla and should read median
HHI 0.275, spread 2.48x, 71 signatures. The second is the tables the authoring
pass wrote, under Ian's level caps, and on 2026-09-23 it read median HHI 0.169,
spread 1.96x, 11 signatures, top slot 25%: flat by design, since the cap replaced
the old concentration arc (design doc 2.5). `main` holds vanilla, and every "does
this match vanilla" check reads `--ref main`. What the second report read before
the pass, and what that proved, is in the archive under M2.

**What exists.** `tools/oxide/encounters/` has `model.py` (loading and slot-level
writing), `analysis.py` (all of section 6's maths, pure functions), `lint.py`
(section 7's rules, every threshold read from the sidecar), `dex.py` (species
names and evolution lines from `res/pokemon/`), `planner.py` (the dupe-out planner,
pure apart from its one loader), `generate.py` (the levels-only generator, pure),
`cli.py` (`areas`, `show`, `set`, `roundtrip`, `sidecar-init`, `report`, `lint`,
`plan`, `generate`), `server.py` plus `ui/index.html` for the browser editor, and
`test_m1.py` through `test_m6.py`. The sidecar is `docs/oxide/encounters/design.json`,
which holds every threshold; the per-playthrough caught record is
`docs/oxide/encounters/caught.json`, gitignored. The modules added since (`audit`, `layout`,
`progression`, `tiers`, `availability`, `locations`, `evolve`, `pokedex`,
`canon`, `calc_export`, `calc_trainers`, `make_calc_skin` and the `test_step*`
suites) are described where they landed, in the archive.

**Where it stands (2026-09-23).** The tool is complete: M1 to M7, and M8's dex,
moves and damage calculator, are done. The authoring pass has written every wild,
water and scripted source from the pick-list, and the tree builds with every table
matching its JSON. What is still open is in "What is open" below. The finished
milestones and steps, with what each one found, moved verbatim to
`docs/oxide/encounter-tool-build-plan-archive.md`, and a one-line pointer stands
where each used to be. The rules still in force from them are in the `author-table`
skill and in "Standing rules" below. The pass's own plan and decisions are
`docs/oxide/encounter-authoring-plan.md`.

**Before running the generator for real**, use `--dry-run` first and read M6's
"one consequence" in the archive: the generator only proposes ladders that obey
R1, so a table whose ladder breaks R1 will change, and it may pay less than it did.

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

## What is open

Every item still open, gathered from the sections now archived and the two below
that stay. None blocks anything.

1. **Maylene's cap.** The tables are designed at 38 and Ian's sheet says 39. They
   wait for the balance track's final caps, then `cli evolve` is re-run once
   (section below).
2. **Ian's one damage roll** in melonDS against the calculator (M8, below).
3. **From the QA pass on D4 and D5** (M8, below): a range check on a trainer's
   `nature` in `trainerproc.c` before Phase 5 names one; the calculator's patch to
   apply a dual type's factors in chart order, which Ian ruled on and which is not
   yet applied or listed in `calc/VENDORED.md`; the four always-critical moves
   shown as placeholders; licence notices for `object_hash` and the ag-grid theme
   CSS; the Z-move twins sharing one calculator name.
   From the balance track (2026-09-25): the calculator's Generation 4 code gives
   no damage for Electro Ball, Heavy Slam, Psywave, Super Fang and Trump Card,
   and the dual-type order above is what puts Crunch into Bronzor at 42 to 50
   where the game says 43 to 51.
4. **The calculator's menu and emulator icons** are missing, since upstream's
   `img/` was never vendored. Cosmetic.
5. **Which trainer Pokemon get a named nature** is Ian's, as Phase 5 balance work.
   How to name one is under "Standing rules".
6. **Other tracks' work this track depends on.** The legendary pool's scripting
   (the two lake caverns as two statics and Mesprit's roamer as a random roamer,
   drawn from one pool of 23) is script work; until it exists R12 reports those
   lines, which is why `lint` shows 27 errors and the gate is `lint --ignore R12`.
   Verity Lakefront's map header still points at no table and the map has no
   grass, and the starter still needs its own met location; both are in the
   tracker's backlog. The same holds for the two tables built ahead of their
   maps on 2026-09-25 (below): Amity Square needs grass and its header, and
   Snowpoint City's header needs pointing at its rods; and the Pastoria City
   gift is to move to the Restaurant. All three are in the tracker's backlog. Deleting the four spare fossil items is item and script
   work. The Day Care Floette's white flower needs a form record and art (tracker
   backlog). Fomantis's data has no evolution to Lurantis, so the tree holds them
   as two lines with a home each until element 3's data is fixed.
7. **Two new capture areas, built ahead of their maps (Ian, 2026-09-25).**
   `encounters_amity_square.json` (grass, Fantina's split, order 36) is a garden
   like the Trophy Garden at very low levels, base level 8, because only small
   Pokemon may walk in with you; `encounters_snowpoint_city.json` (the three rods
   only, Candice's split, order 101) fishes at Lake Acuity's levels. Both casts
   are drafts for Ian to change in the tool. Both files are appended to
   `encounters.order`, so no existing table moves in the NARC, and until a header
   uses them the sidecar's new `planned_location` key names the capture area
   they count as (Verity Lakefront's entry now carries it too). With them the
   count of captures before the League is 69 by location name, 73 once the three
   maps and the Restaurant move exist (`docs/oxide/encounters/scripted-sources.md`
   has the working).
8. **The Galactic split and the Battle Zone (Ian, 2026-09-25).** The split table
   gains Galactic between Candice and Volkner, cap 64, and Volkner's cap is 68.
   The ten Battle Zone tables and the eleven tables of the Mt. Coronet climb are
   in it, and the Battle Zone follows Snowpoint in progression order. The ten
   tables were authored in Step 4 as post-game content, and in their new split
   they pass every lint rule and the availability gate unchanged; what they
   offer before Volkner (Metagross at 10% on Route 228, the fully evolved
   starters as 1% tails) is put to Ian rather than changed. Waiting on the
   balance track, whose tool must learn the new split before this merges. The
   whole plan, across the three tracks, is `docs/oxide/battle-zone-plan.md`.
9. **One-spot groups (Ian, 2026-09-26).** A place whose tables sit in one spot
   is now identical throughout or very different part to part, as the sidecar's
   `groups` table says and lint's R15 enforces; the `author-table` skill has the
   list. Mt. Coronet became five capture areas (`capture_area` in the sidecar),
   Oreburgh Gate B1F moved to Gardenia's split, Coronet B1F and North Room 2 to
   Candice's, and Victory Road's three side rooms to post-game. The area list
   folds each group under one row and files each area under the earliest split
   it can be caught in (Route 218's Old Rod water sits in Roark's). Captures
   before the League: 73 today, 77 once the planned maps exist, 85 with the
   Battle Zone open before the League.
10. **The top rung (Ian, 2026-09-26).** Every table from Gardenia's split to
   the League had a top rung one or two lines wide, so a max-level manip was a
   guaranteed prize or a coin flip between two. Those 105 tables now lay out in
   their archetype's top form: a lead at the highest level meets one ordinary
   line 80% of the time and two others 10% each. A19 casts lost one of their two
   4% lines to make room; Route 204 North, Wayward Cave and Victory Road's 1F
   and 2F, whose faces were prizes, now lead with an ordinary line. Lint's R16
   enforces it; Roark's split, where repels are scarce, and the post-game keep
   the old shapes.
11. **Honey trees by split (Ian, 2026-09-26).** The trees read one table per
   badge count, 1 to 8, each with a common and an uncommon tier of six and its
   own level range (10-14 at one badge up to 45-50 at eight), picked when the
   tree is shaken. Every tree rolls nothing 10%, common 70%, uncommon 20%: the
   four Munchlax trees and their rare tier are gone. This track made the engine
   change in `src/overlay005/honey_tree.c` and `src/overlay006/wild_encounters.c`
   with Ian's say-so. Rowlet, Snivy and Sprigatito left the trees for land homes
   at 10% (Eterna Forest by day, Route 204 north, and Route 210 south, where
   Floragato took Swablu's 10 and Smoliv dropped to a 1%). The eight tables are
   a first draft for Ian: bugs and tree dwellers, Heracross climbing from a 1%
   to the head of the uncommon tier. The GitHub build of e18209dc1 carries the
   eight tables at `encdata_ex` member 2 and passes test_step0 against it;
   waiting on a shake in game at one badge and at five.
12. **Scripted captures and honey trees in the area list (Ian, 2026-09-26).**
   `docs/oxide/encounters/scripted.json` names every gift, trade, static,
   fossil and egg with its capture area, split and play order; `scripted.py`
   takes the species and levels from the sources catalogue. Each one is a row
   in the list, in play order, markable as caught, and it spends or shares
   its place's capture like a table does. An egg is a capture of its own,
   since it counts where it hatches. A table whose map has a honey tree shows
   the tree's table for its split, with boxes to tick the catch.
13. **The box simulator (Ian, 2026-09-26).** The Box sim tab plays one run to
   the end of a chosen split, with a number of deaths and a starter, and
   shows it area by area with the box it ends with; Regenerate plays another.
   `simulate.py` holds the rules and the per-area analysis (`--areas SPLIT`).
   A Pokemon's worth mixes the BST of the stage it reaches by the cap, a
   nuzlocke rating per line and its pick-list tier. The ratings are
   `docs/oxide/encounters/values.json`, a first draft for Ian to correct; the
   balance track has no per-Pokemon value to borrow, since its pressure
   scores are per fight. The player is greedy and adaptive, and it waits
   for a later table when that is worth more. It also places the one early
   repel where it gains most. A random gift is read as declinable under the
   dupes clause. `test_sim.py` pins the rules.
14. **Ian's second pass on the scripted sources (2026-09-26).**
   `scripted-sources.md` has what changed. The weak points were: early
   gifts too strong, the Windworks Drifloon balloon, and lines the player can
   always have also sitting in tables. Riley's egg is one of eight lines at
   random. Mindy trades a shiny Suicune (Serious, 15 across) for a Snover.
   The legendary pool is dealt into three thirds, one each for Acuity
   Cavern, Valor Cavern and the roamer.
15. **Seventeen water lines (Ian, 2026-09-26).** Clamperl, Corsola, Horsea,
   Krabby, Lapras, Poliwag, Psyduck, Qwilfish, Relicanth, Seel, Shellder,
   Slowpoke, Spheal, Staryu, Totodile, Wailmer and Wingull are on the
   pick-list. Their 37 rows are appended at its end, so no existing dex
   position moved; where they sit in the regional dex is Ian's call. The
   57 water slots the Popplio strip left waiting went to them, by the water
   they are in (sea, lake, the cold north) and by the slot's size. Each line
   has a home at a real share and a second appearance. Toxapex is back from
   Byron's split on, since it is too strong only earlier. Snowpoint's harbour
   is iced over: Spheal and Seel at home, Shellder, Lapras the prize, and
   Snorunt, Swinub and Froslass up through the fishing holes. That is the
   first fishing table with lines that are not Water type where the theme
   calls for it, which Ian wants more of. Froakie has two 4% slots beside
   its Old Rod tails. In Ian's sample boxes Route 223 and the Pokemon League
   came up empty, every line there already in the box. Route 223 was empty
   in 31 of 40 simulated League runs before these lines and in none after;
   `test_sim` now fails if an area goes dead.
   - **The Route 226 trade is to become Meloetta** (Ian): it needs work
     later, since Meloetta is not in the species tree. Until then the trade
     stays as it is, and its Magikarp still breaks the rule that a line the
     player can always have is in no table.

## Standing rules

The authoring rules (splits, caps, width, the evolution pass, the no-leak rule
and the whole-game gate) are in the `author-table` skill. These are about the tool
itself.

- Run the suites one at a time. `test_step0` rewrites shared files under a
  restore, and every test restores by writing back the text it saved, never by
  `git checkout --`, which once reverted Route 214's uncommitted table.
- A new way of authoring a table (a new sidecar key, a new file kind) extends
  `authored_encounters()` in `tools/oxide/import_base_rom.py` and `test_step0`'s
  mirror of it in the same commit, or the importer's dry run reverts the table
  (design doc findings log, 2026-09-21).
- Every checkout and worktree has its own copy of the server and all want port
  8765; the header names the checkout it reads, and `--port` runs a second one.
- A trainer Pokemon names its nature with `"nature": "NATURE_ADAMANT"` (any of
  the 25), which frees its IV scale to go to 255; a member without the field
  rolls exactly as before. Do not name `NATURE_COUNT`: until the range check in
  item 3 lands, the game loops forever building that party. How it works and how
  it was checked are in the archive under M8.
- The vendored calculator is a clean upstream copy plus the patches listed in
  `calc/VENDORED.md`; after an update, re-apply them and rerun
  `make_calc_skin.py`, and `test_m8` fails until both are done.

## The milestones

All seven are done. Each one's section, with its gate and what it found, is in `encounter-tool-build-plan-archive.md` under the same heading.

- M1, round-trip I/O: done 2026-09-20.
- M2, analysis engine: done 2026-09-20.
- M3, linter: done 2026-09-20. Its outcome sorts the thresholds into descriptive and aspirational.
- M4, the UI: done 2026-09-20, with Ian's three rounds of usability notes the same day.
- M5, dupe-out planner: done 2026-09-20.
- M6, generator, levels-only: done 2026-09-20. Full species placement is deferred, possibly for good.
- M7, ROM verification: done 2026-09-20.

## Authoring pass

Status for `docs/oxide/encounter-authoring-plan.md`, gate by gate. The plan
says what each step is; this says what happened.

Steps 0 to 8 are done, and each step's entry is in `encounter-tool-build-plan-archive.md` under the same heading:

- Step 0, tooling: done 2026-09-20.
- Step 1, order and tiers: done 2026-09-20.
- Step 2, the availability plan: done 2026-09-21.
- Step 3, the first two splits: done 2026-09-21, after two regenerations on Ian's review.
- Step 4, the rest of the game: done 2026-09-21.
- Step 5, the no-leak pass: done 2026-09-21.
- Ian's follow-ups after Steps 4 and 5: done 2026-09-21.
- Step 6, build, verify, merge: done 2026-09-21.
- Step 7, the scripted sources, and four notes from Ian: done 2026-09-21.
- Step 8, stages, trades and the last two menus: done 2026-09-21.
- Ravaged Path is Roark's split: done 2026-09-22.

### Maylene's cap: 38 in the tables, 39 in Ian's sheet (known, waiting)

A known mismatch, written down on Ian's ruling of 2026-09-22. Every table in
Maylene's split was designed against a level cap of 38, the figure from his
second review (above). His Level Caps sheet says 39, and the balance track
found the difference (question 5 in `docs/oxide/balance-plan.md`). Ian settled
it in the sheet's favour, but ruled **not to change the tables now**: the
balance track is redesigning the whole cap curve first and taking it to him.
Until those final caps land, the tables stay as designed at 38. Then they
re-run `cli evolve` once against the final caps (the evolution stages are the
only part of a table that depends on a cap), with the suites and the source
check after it, rather than moving for 39 now and again later.

Two later entries are done and archived in `encounter-tool-build-plan-archive.md`: Ian's notes on the Tables view (2026-09-22) and the QA pass before the merge (2026-09-22).

## M8, the dex and the damage calculator: **done 2026-09-22, one in-game roll to check**

Done except for what follows. The survey, D1 to D5, the trainer teams in the calculator, trainer natures, and the decisions and risks recorded before starting are in `encounter-tool-build-plan-archive.md` under the same headings.

### What is open in M8

**Open from the QA pass before the merge** (2026-09-22,
`docs/oxide/qa-review-2026-09-22-encounter-d4d5.md`; none of it blocked the
merge). The trainer packer accepts `"nature": "NATURE_COUNT"`, and the game
then loops forever building that party, because no personality lands on a
26th nature; a numeric or `true` nature is dropped without a word. It needs a
range check in `trainerproc.c` before Phase 5 names a nature. The calculator
applies a dual type's two factors in the defender's type order where the game
uses chart order, so Crunch into Bronzor reads 42 to 50 against the game's 43
to 51; this is upstream's behaviour, and **Ian ruled (2026-09-22) that the
calculator follow the game's chart order**, so it is this track's next patch
to the vendored calculator (as of 2026-09-23 neither applied nor yet in
`VENDORED.md`'s patch list). The four always-critical moves (Flower Trick,
Frost Breath, Storm Throw, Wicked Blow) are listed as placeholders, because
element 4 did their effect in C and left the script a plain hit. `object_hash`
and the ag-grid theme CSS came in with no licence notice. Smaller: the Z-move
twins share one calculator name, so one overwrites the other.

**What is left is Ian's:** one roll in the game against the calculator. In
melonDS, note an attacker's and a defender's level, stats and the damage a
move does. Enter the same two in the calculator, then check the damage falls
in its range.

The visual design (palette B, built and signed off by Ian on 2026-09-22) and the original "Suggested order, and what to cut" are archived in `encounter-tool-build-plan-archive.md`.

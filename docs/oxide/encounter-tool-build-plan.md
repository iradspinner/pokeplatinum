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
PYTHONPATH=. python3 -m tools.oxide.encounters.test_m8     # expect 94/94, the dex, moves, calculator and trainer sets
PYTHONPATH=. python3 -m tools.oxide.encounters.test_step0  # expect 35/35
PYTHONPATH=. python3 -m tools.oxide.encounters.test_step1  # expect 21/21
PYTHONPATH=. python3 -m tools.oxide.encounters.test_step2  # expect 18/18
PYTHONPATH=. python3 -m tools.oxide.encounters.test_step3  # expect 36/36
PYTHONPATH=. python3 -m tools.oxide.encounters.test_step5  # expect 19/19
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
3. **From the QA pass on D4 and D5** (M8, below). Closed. The last item,
   taken by this track on the Overseer's word on 2026-09-27: the importer
   skipped the IV scale of a member that names a nature without saying so,
   and now its report names each such member ("party[i].iv_scale: names
   NATURE_X, left alone"), as it names every other divergence; the line is
   report text only and changes no count. On 2026-09-26 the calculator
   took the chart order (Crunch into Bronzor now reads the game's 43 to 51,
   and Cross Chop into Bronzor 80 to 96, not 81), the engine's damage for
   Heavy Slam, Trump Card, Psywave and Super Fang, and the always-critical
   moves, which the dex no longer lists as placeholders; the vendored
   libraries got their licence notices (`calc/VENDORED.md`, patches 9 to
   12). Electro Ball's power is item 22's. Later the same day, on branch
   `encounter-item3`:
   - The trainer packer refuses a `nature` that is not one of the 25:
     `NATURE_COUNT`, which would have hung the game building the party, an
     unknown name, a number and `true` each fail the build at the line, and
     null still means roll it. The packer's seven outputs for the whole tree
     are byte-identical to the unchecked packer's. dataproc's own range
     check (`dp_u16range`) cannot be used on a looked-up name: the node's
     source position and the looked-up value share one field, so the error
     report reads the value as a pointer and crashes. The packer compares
     the value itself, and `itemproc.c` has the same pattern for a TM's
     type, which never fails today.
   - The calculator's data holds all 919 moves. Each of the 18 Z-moves is a
     physical and a special twin in Oxide and one entry in the calculator;
     the physical keeps the calculator's name and the special is exported
     as "Breakneck Blitz (Special)" and so on. `calc_export.move_keys` is
     the one place that names a move, and the mechanics lists use it too.
   - Two stale comments from the same QA: species weight is in pounds, and
     the calculator's images come from `res/pokemon/`.
4. **The calculator's menu and emulator icons.** Done 2026-09-26: the menu icon
   is the tool's own, and the DeSmuME link is hidden under Oxide (patch 13).
5. **Which trainer Pokemon get a named nature** is Ian's, as Phase 5 balance work.
   How to name one is under "Standing rules".
6. **Other tracks' work this track depends on.** Most of it landed with
   `pool-base` (2026-09-27), merged here: the legendary pool's draws are
   scripted (Acuity Cavern once per save and Mesprit's roamer; Valor Cavern
   and Stark Mountain's last room empty, item 21), the starter's met location
   is its own ("Rowan's Briefcase", so Route 201 is a capture from the first
   step and the simulator no longer spends it on the starter), Verity
   Lakefront, Amity Square, Snowpoint City and the four clown towns point
   at their tables, the gift clowns are gone, and Fomantis evolves into
   Lurantis at 34, so the two are one line (238 lines on the list; Route
   224's Fomantis slot became Tropius, and Route 221's Lurantis a cameo, the
   line's home being Route 208). R12 read gifts from `pokemon-gifts.csv`,
   a survey of the base ROM of 2026-09-20, with a starter list naming
   Chimchar and no sight of the pool draws, so it showed 35 errors, among
   them lines Oxide does hand over (Scorbunny, Elekid, Flabebe, the Acuity
   draw). **Fixed on 2026-09-27** (item 27): it reads Oxide's own sources,
   and Stark Mountain's hidden Heatran is no source while the room is empty
   (`UNREACHABLE_SCRIPT_SOURCES`, which the sources catalogue honours too).
   The gate stays `lint --ignore R12` until Ian has been through the real
   errors that remain. Some flags are real and are
   for Ian: with the babies at level 10 no wild Pichu or Cleffa is left, only
   Pikachu and Clefairy. Deleting the four spare fossil items is item and
   script work. The Day Care Floette's white flower needs a form record and
   art (tracker backlog).
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
   Superseded on 2026-09-26: the Galactic fights are two splits, HQ at cap 60
   and then Galactic at 65, and the split table has had them since.
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
   Battle Zone open before the League. Wayward Cave moved from "same" to
   "distinct" later that day, at Ian's request: 1F is the dark cave
   (Carbink, Bronzor, Zubat and the rock lines, Nacli and Bonsly at 1%),
   B1F the sand floor under Cycling Road (Phanpy leads, Gible's 10% morning
   home, Sandygast, Glimmet, Stunky, Larvitar at 1%). They share Nacli and
   Zubat, and the cave is still one capture.
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
16. **Strong Pokemon made scarce, step 1 (Ian, 2026-09-26).** No Pokemon
   worth about 85 or more (the simulator's value) should be better than even
   odds with best play; a box entering the Elite Four should hold one to
   three, not a party. Best play used to end the League with a median of
   nine: Giratina, the two eggs and Gyarados in every run, Garchomp and
   Tyranitar in 98%, Metagross in 85%, Mamoswine in 80%. Step 1:
   - Giratina in the Distortion World is not a legal catch.
   - Gible, Beldum and Swinub keep one or two capture areas each (Wayward
     Cave, Iron Island, Route 217 and Mt. Coronet North). Larvitar is a 1%
     beside Gible at Wayward Cave, so one capture yields at most one of the
     two. Magikarp keeps one 4% or 1% Old Rod slot on Lake Verity, Route 203
     and Route 212 south.
   - Everywhere else each gave way to a line of the same kind the table
     lacked, never one worth 80 or more, and no line took more than four
     slots.
   - The Route 226 trade leaves the simulator until it becomes Meloetta.

   Over 40 League runs the median is now four, and no line passes half:
   Garchomp 32%, Mamoswine 18%, Tyranitar 12%, Metagross 5%, Gyarados
   never. The four are the two eggs, which Ian accepts, and one legendary
   from each lake cavern. `test_sim` pins the rule over 20 runs.

   What the simulator showed along the way: late in a run the dupes clause
   inflates any prize whose table's other lines the box already owns. A 1%
   Pupitar beside a Crobat anchor became a coin flip by Candice's split,
   since nearly every box has a Zubat. So scarcity comes from fewer
   appearances and from prizes that compete in one capture, not from
   smaller slots. The tier just below, 75 to 85, still lands a median of
   29 per box, a dozen lines in every run. Next: Ian's call on step 2.
18. **Step 2 of the scarcity work (Ian, 2026-09-26).**
   - The two lake caverns give no legendary for now.
   - The Magikarp line is cut from the pick-list (`cut`, so no id moves).
   - The pick-list is at Platinum's size: 493 species in 239 lines, up
     from 420 in 205. Ian's criteria were cute lines, a type spread across
     the game, zone themes and vanilla Platinum staples. The 34 new lines:
     Starly, Bidoof, Kricketot, Wurmple, Abra, Machop, Burmy, Cherubi,
     Chatot, Chingling, Hoothoot, Murkrow, Aipom, Munchlax, Magnemite,
     Cleffa, Azurill, Happiny, Mime Jr., Bonsly, Lickitung, Tangela,
     Meditite, Girafarig, Carnivine, Tropius, Snubbull, Mawile, Plusle,
     Minun, Delibird, Smoochum, Mareep and Hoppip.
   - Each new line took the slot of a widespread line in a table that
     suits it, and the honey trees took the vanilla honey lines.
   - A line may now live only as cameos or tails below the 10% a home needs.

   Best play ends the League with a median of three Pokemon worth 85 or
   more. The tier from 75 to 85 still lands a median of 29 per box, and 28
   of its lines land in over half of runs; trimming it waits on Ian's
   super-wanted list.

   Ian's super-wanted list came next. It is recorded in `values.json`
   (`wanted`): Vulpix, Ponyta, Koffing (both forms, regional preferred),
   Eevee, Togepi, Articuno (Kanto only), Suicune, Ralts, Skitty, Roselia,
   Swablu, Milotic, Froslass, Buneary, Drapion, Cresselia, Florges,
   Primarina, Tsareena, Pheromosa, Cinderace, Corviknight and Meloetta. A
   majority should land in a run, they are never trimmed, and their
   legendaries are the ones kept. The simulator now plays towards them: a
   bonus on its choices, never on the reported worth.

   The trim cut fifteen prize-kind lines to their planned home, or to their
   rarest place: the scattered starter tails, Kommo-o, Goodra, Flygon,
   Scizor, Hippowdon, Slowbro, Walrein and Cloyster.
   - Their other slots went to wild lines of a shared type worth under 75,
     never a scripted-only one.
   - The early Old Rods keep their starter tails.
   - Torchic keeps Route 204 north's day slot, the delay.
   - Froakie keeps its extra slots, as Ian asked.
   - The zone staples (Zubat, Bronzor, Gligar, Sneasel, Rhyhorn, Gastly,
     Duskull) stay: trimming them would strip the caves.

   Over 30 League runs, non-wanted lines worth 75 or more fall from a median
   of 26 per box to 18, and a median of 15 of the 23 wanted lines land. The
   five that never do are out of the simulator's reach: Articuno and
   Cresselia are post-game, Meloetta is not in the tree, Pheromosa sits in
   the roamer's third, and Suicune needs a planned Snover. Still in over
   half of runs: the staples, the homes of Hippowdon, Cloyster, Walrein and
   Flygon, Froakie's Greninja, and the Veilstone Elekid, the Elekid line's
   only source.
19. **The damage calculator learns element 5's abilities (Ian, 2026-09-26,
   through the Overseer).** The vendored calculator's Generation 4 branch
   applies only Generation 4 abilities, so element 5's damage-changing ones
   count nowhere: not in the tool's calculator, not in the balance scores.
   Among them are Water Bubble, Fluffy, Purifying Salt, Steelworker, Sap
   Sipper, Pixilate, Sheer Force, the auras, and Sharpness with
   hg-engine's longer slicing list including the five claw moves. The
   reference is element 5 on oxide (`git log 2f8d27c3^..a51b0af3`) and its
   report on `cloud/element5-abilities`. It sits beside the three
   calculator defects already held, closes before the trainer pass, and the
   balance track rescores after it.
   **Done 2026-09-26** as a Platinum Oxide romhack profile in the calculator
   (`calc/VENDORED.md`, patch 9), with its move lists generated from
   `battle_lib.c` by `make_calc_mechanics.py` and pinned by `test_m8`.
   Neutralizing Gas is a battle state, not a matchup, so it is not modelled;
   blank the ability by hand to see it. The balance track's rescore is
   pending, and its `test_b3` pins the two Bronzor ranges at the old numbers.
   The staples rulings that change damage followed on 2026-09-26, once the
   engine had them: critical hits at 1.5x, Simple, Normalize, Lightning Rod
   and Storm Drain, Grass against powder moves, Sturdy, and the four new
   Intimidate blockers. Native moves take their numbers from `res/`, so
   they needed nothing. The calculator shows damage, not odds, so the new
   critical hit rates and Keen Eye's accuracy are left to the balance
   track's models. The list as it stood before:
   - critical hits at 1.5x and the modern rates
   - the Gen 6 type immunities: Grass against powder moves, Electric
     against paralysis
   - modern behaviour for native abilities (Sturdy, and Lightning Rod and
     Storm Drain first)
   - native moves at their full modern numbers after the data pass
21. **The missing super-wanted lines (Ian, 2026-09-26).** Five of Ian's 23
   never landed in a best-play run. Ian took this, with Mindy asking for a
   Snover ("four strong is fine"). Measured over 30 to 40 League runs:
   - Acuity Cavern returns, drawing one of Ian's three most-wanted
     legendaries at random: Articuno, Cresselia or Pheromosa. Valor Cavern
     stays off. The lines Acuity drew before wait in the pool's `reserve`.
   - The simulator plans for a trade whose gift is wanted. It values the
     species asked for (Mindy's Snover) as if it were wanted, and treats a
     member caught for the trade as its price, not a loss.

   A median of 17 of the 23 land and only Meloetta never does. The price is
   a median of four Pokemon worth 85 or more per box, up from three,
   because Suicune lands in 97% of runs. If Mindy asks for a rarer line
   (Delibird was tried) Suicune all but vanishes and the median stays
   three. Meloetta needs porting before it can be placed.

   **Ian, 2026-09-27, relayed by the Overseer:** Valor Cavern holds no
   legendary at all, Azelf included, and Stark Mountain's last room is empty
   (no Heatran, no draw), both until the difficulty is high enough that more
   legendary-tier encounters would not inflate box quality. Acuity Cavern
   stays a once-per-save draw of the three, shown with Uxie's sprite for
   now. `scripted.json` marks both places empty and out of the simulator,
   the pool's comment in `availability-plan.json` carries the condition,
   and `availability.md` now says a run meets two pool legendaries before
   the League. The main track is scripting Acuity's draw and the roamer's.
22. **The calculator follows element 4's variable powers (Ian's Overseer,
   2026-09-26), queued until the balance track's running rescore merges,
   so the next rescore takes it in one go.** oxide 48596e2bd computes
   Electro Ball's power from the Speed ratio (40, 60, 80, 120, 150), and
   Stored Power, Power Trip, Retaliate, Echoed Voice, Stomping Tantrum,
   Temper Flare, Last Respects, Hard Press, Pika Papow, Veevee Volley,
   Lash Out and Grav Apple in code (the report is the last commit on
   `cloud/element4-variable-power`). The profile's Electro Ball at power
   1 goes, and each of the others follows the engine as far as a single
   matchup can show it. In the same pass, Freeze-Dry and Flying Press stop
   taking their later-game type effects, which upstream's shared
   `getMoveEffectiveness` gives them in every generation: Oxide's engine
   hits with both as plain moves until the main track fixes the moves that
   choose another stat or type in C. Measured on 2026-09-26, the
   calculator puts Freeze-Dry into Vaporeon at 80 to 96 and Flying Press
   into Abomasnow at 268 to 316, about four times and 1.6 times what the
   game does. Foul Play, Body Press, Psyshock, Sacred Sword and Darkest
   Lariat already hit as plain moves in the calculator's Generation 4 code.
   **Done 2026-09-26, and merged on 2026-09-27 with the balance track's
   rescore** (68eebf653), from branch `encounter-calc-item22`.
   Electro Ball, Stored Power, Power Trip, Hard Press, Last Respects (from
   the calculator's fainted-allies field), Grav Apple under Gravity, and
   Pika Papow and Veevee Volley at Return's 102 follow the engine; the five
   that depend on an earlier turn keep their table power, which is the
   engine's when the condition is not met. Freeze-Dry and Flying Press hit
   as plain moves, and `test_m8` pins both. When the main track gives them
   their type rules, the `util.js` patch (`VENDORED.md`, 11) comes out.
23. **The calculator follows the engine's stat and type choices (Ian's
   Overseer, 2026-09-26), queued until `cloud/element4-stat-choice`
   merges**: Foul Play, Body Press, Psyshock, Sacred Sword, Darkest Lariat,
   Freeze-Dry, Flying Press and Rage Fist (50 plus 50 per hit taken, to
   350). It builds on item 22 and takes out item 22's `util.js` patch for
   the two type moves. The Generation 4 path has hooks for an attacking
   stat's size but not for whose stat or which defence stat a move reads,
   so it gains one; the rules come from the merged engine, not from canon.
   **Done 2026-09-27** on `encounter-item3`, after the engine merged
   (6e729d2c0). Two new hooks in the Generation 4 path (`VENDORED.md`, 10):
   `attackSource` gives Foul Play the target's Attack and stages, past its
   Unaware, and Body Press the user's Defense and stages, with the user's
   own attack modifiers kept; `defenseSource` sends Psyshock, Psystrike and
   Secret Sword against Defense with the Defense modifiers and not the
   Sp. Def ones (sandstorm's Rock boost among them, as the engine swaps the
   stat after its modifiers), and has Sacred Sword, Darkest Lariat and Chip
   Away ignore the target's stages. Item 22's `util.js` exception is gone:
   upstream's Freeze-Dry and Flying Press rules are the engine's now. Rage
   Fist shows 50, the engine's power before any hit, since the calculator
   has no field for hits taken. `test_m8` 94/94 pins each rule with rolls
   that do not depend on Oxide's stats. The balance track rescores after it.
24. **Friendship evolutions replaced (Ian, 2026-09-27, through the
   Overseer).** Happiness Up is gone, and every friendship evolution moves
   to a method that cannot be ground. The proposal, one method per line
   with its split and what it changes here, is
   `docs/oxide/encounters/friendship-evolutions.md`. **Ian accepted it on
   2026-09-27 with Crobat at level 40** (Wake's split), and one fixed Sun
   Stone and Moon Stone find for the balance track's item pass to place.
   The main track edits the evolution data. Once that merges, this track
   reruns `cli evolve` (with Maylene's cap if it has landed), puts the
   seventeen Crobat placements below 40 back to Golbat by hand, corrects
   the evolve tool's judged levels, which have read every
   friendship method as 32 and a held-item trade as 32 because they are
   keyed by names the data does not use, and reruns `test_sim`. **Done
   2026-09-27 on the `pool-base` data:** the nine slots evolved (four Pichu,
   three Buneary, the Coronet Cleffa, the Great Marsh Azurill), the
   seventeen Crobat placements are Golbat again, species only with every
   level kept, and the evolve tool's judged levels are keyed by the data's
   own method names (no friendship or trade method is left, so the values
   are unchanged). The Azurill line, now fully evolved by 18, became a cap
   candidate in Gardenia's split, so Route 205 north's Pachirisu slot is a
   Marill. `cli evolve` reports 0 moves.
25. **Thorton's encounter and Argenta's reward (Ian, 2026-09-27, through
   the Overseer)**, for the Frontier Brains in Byron's split. The proposals
   are `docs/oxide/encounters/frontier-brains-rewards.md`: a level-40
   Cinderace static at the heart of Fuego Ironworks, sharing the yard's
   capture, with a Battle Factory rental draw as the alternative; for
   Argenta, items if the box should not grow, or an egg drawn from Happiny,
   Smoochum and Elekid. **Ian ruled on Thorton (2026-09-27):** the player
   picks one of the two starter lines they did not choose, fully evolved at
   level 40, as a Battle Factory rental sharing the Fuego Ironworks
   capture. Argenta stays open between items and a level-40 static. The box
   sim measurement of Thorton's prize follows the balance track's rescore.
   **Later on 2026-09-27:** the prize gets a capture of its own (the
   Ironworks building gets its own location name, so 76 captures before
   the League), and Argenta's reward is items, picked by the balance
   track's item pass. Redone once the building had its name, "Ironworks
   Hall": the prize is `ironworks_hall_thorton` in `scripted.json`, a
   planned source, and as its own capture it adds a whole wanted line for a
   Turtwig or Piplup start and no line worth 85 or more (the doc has the
   table).
26. **The gift clowns go (Ian, 2026-09-27, through the Overseer).** A clown
   whose capture area has a table, gift or trade simply goes; otherwise new
   tall grass with a thematic table takes its place. This supersedes the
   tracker's backlog item to unify the clown gifts. The proposal, per area,
   is `docs/oxide/encounters/clown-replacements.md`: new grass in Sandgem
   Town, Jubilife City, Floaroma Town and Solaceon Town, which homes seven
   thinly sourced lines (Kricketot, Abra, Combee, Tropius, Happiny,
   Girafarig, Lickitung) and the two clown-only ones (Poochyena, Trapinch);
   the Oreburgh, Floaroma Meadow, Veilstone and Restaurant clowns and the
   Eterna condominium gift simply go. **Ian accepted it on 2026-09-27**:
   the Canalave Library gift goes too, with Mankey homed in Solaceon's
   grass; Charcadet gets a 10% home on Route 206 and in Fuego Ironworks'
   yard (the doc's last section); grass is tile behaviour first; and
   capture levels end at about 60, which the tables already do (land tops
   out at 54, the Super Rods at 60; only the post-game Dialga and Palkia,
   at 70, are higher). The main track does the maps and scripts; this
   track writes the four tables once the grass exists. Charcadet's two
   slots needed no grass and are in the tables (2026-09-27): Route 206's
   10% (Dwebble to the 1%) and the Fuego yard's at 29 (Togedemaru out),
   with the Fuego yard as the line's planned home and Ceruledge on Route
   227 a cameo. **The four tables are written** (2026-09-27), built ahead
   of their headers like Amity Square's, as `encounters_sandgem_town`,
   `encounters_jubilife_city`, `encounters_floaroma_town` and
   `encounters_solaceon_town`, appended to `encounters.order` so no table
   moves in the NARC; the main track points each header at its table.
   Each is an A19 with `planned_location` set. Three departures from the
   proposal, forced by the layout and the evolve rule: A19 keeps its face
   at 20% and anchors its 4%s on another line, so Pachirisu (Floaroma) and
   Mareep (Solaceon, a Flaaffy at 22) take the top rung; Poochyena is a
   Mightyena at Solaceon's levels, so its home is Floaroma's 10% and
   Solaceon has Mightyena; and Trapinch's planned home moves from Route
   228 to Solaceon, which clears it from the cap candidates. The ten
   retired gift sources left `scripted.json`. Suites: m1 13/13, m2 23/23,
   m3 18/18, m5 15/15, m6 19/19, m8 91/91, step1 21/21, step2 18/18,
   step3 35/35, step5 19/19, sim 11/11 (their counts and the clown checks
   brought up to date); test_m4 and test_step0, which rewrite shared
   files, were left to the gate while Ian has the server open.
27. **R12 reads Oxide's sources; the classic starters and Surskit (Ian,
   2026-09-27, through the Overseer).** On branch `encounter-r12-sources`,
   after 316afcc01. R12 and the availability gate now read gifts from the
   tree's scripts, the runtime picks from `scripted.json`'s live sources and
   the pool draws from the new-game script, where they read the base ROM's
   survey of 2026-09-20; R12 falls from 35 errors to 30, all real. That
   exposed three things. Ian ruled that the classic starters leave the gate
   tier and become ordinary wild lines; their placements are proposed in
   `docs/oxide/encounters/classic-starters.md` and wait on him (Charmander
   on Route 211 west, Squirtle on Route 205 north, Torchic on Route 205
   south, Mudkip on Oreburgh Gate B1F, Treecko staying on Route 204 north).
   Surskit is retiered to starter-adjacent, so its Lake Verity home stands
   in Roark's split. And Verity Lakefront's night slot, which held
   Poochyena on the strength of the Floaroma clown, is Kricketot. Until the
   starters go in, the gate's one complaint is Squirtle and Mudkip without
   a source, so three suites fail on this branch; it merges after the
   placements, as a small incremental rescore. **Ian approved the rarer
   shapes on 2026-09-27, and they are in**: the fifteen rows leave the gate
   tier for preferred; Charmander is a 5% slot on Route 211 west, Mudkip a
   5% slot on Oreburgh Gate B1F, Treecko one morning slot on Route 204
   north (Budew has the other), Squirtle by day on Route 205 north, Torchic
   by day on Route 204 north as before. A single slot inside a line's share
   is not something an archetype can express, so the sidecar gains
   `slot_species` (slot index to species, set after the layout at the
   ladder's level), tested in test_step3. Route 212's Shellos and Gastrodon
   are the West Sea form (Ian, the same day). The gate passes; R12 shows 27
   errors, every one either a pool line drawn nowhere, a proposal, a baby
   now standing as its next stage, or a slot its land-only cost model does
   not price (Squirtle's and Torchic's day finds among them).
28. **The trainer team builder (Ian, 2026-09-27, through the Overseer).** A
   new tab: pick any of the 928 trainers, edit the team, and save straight
   into `res/trainers/data/<stem>.json` in the file's own style, so each
   change is an ordinary git diff. Scoped here; the build starts on a branch
   from `oxide` once the landing has moved it.

   **What it edits.** Per Pokemon: species, form, level, the four moves,
   ability, held item, nature and IVs. Per trainer: the AI flags and whether
   it is a double battle. Three limits of the format shape the page:
   - The ability field is 0 (either ordinary slot, by personality), 1 or 2.
     A trainer Pokemon has no hidden slot: nothing in the trainer code calls
     the engine's hidden-ability function. Offering it needs 3 in the
     packer's range, that call in `src/trainer_data.c`, and
     `calc_trainers.build_trainer` mapping 3 to the calculator's hidden
     slot, which the balance scorer then follows with no change of its own.
     The Overseer gave the engine side to the main production agent, whose
     `main-trainer-hidden-ability` (1832a346c) takes 3, keeps the
     personality as 0 does, and gives the record's hidden ability or leaves
     the ordinary one. This track's side is done on
     `encounter-trainer-hidden` (00e2365ac, cut from that branch):
     `calc_trainers` reads 3 the same way, and reads a form's ability from
     the form's own record, which it had not done since f801cc160. Ian's
     staples answer 9, Drizzle on Pelipper and Drought on Torkoal for
     trainers only, needs the slot, and also needs those hidden slots set:
     in `res/` today Pelipper's is Rain Dish and Torkoal's Shell Armor.
   - IVs are one number for all six stats: the IV scale, 0 to 255, gives
     each IV as `scale * 31 / 255`, and the page shows the IV it gives.
     Per-stat IVs would be a format and engine change, which was not asked.
   - The packer reads the first member to decide whether a party carries
     items and moves, so a save keeps every member's keys alike, and giving
     one member moves on a trainer without them writes them for all.

   The nature field is safe to save already. The packer refuses
   `NATURE_COUNT` and anything but the 25 names, and null still means
   rolled (item 3); that landed with `encounter-item3`.

   **How it saves.** Each changed field is replaced in the file's text with
   `jsonstyle`'s helpers, never a reformat; a first nature goes in with
   `insert_key`; a changed party size rewrites the party array with
   `jsonstyle.dumps`, corrected for its one known miss (a two-move list,
   which the repo writes a move a line). A test loads and saves all 928
   files unchanged and expects every byte back. On every save:
   - the trainer lint below runs, and an error refuses the save;
   - the real packer (`build/tools/dataproc/trainerproc`) packs the tree
     into a scratch folder, so anything the build would reject shows at once;
   - the trainer is registered as an intended divergence, or the gate's
     base-ROM check carries the base ROM's team back.

   `TRAINERS_DIVERGED` is a Python dict in `import_base_rom.py`, and a save
   cannot append to code cleanly. The proposal is a data file beside it,
   `docs/oxide/trainers-diverged.json` (trainer, field, reason), which the
   importer merges into the dict: a first team edit writes `"party"`, and
   an AI flag or double battle edit writes that field. The importer honours
   a divergence for party fields and the name today, not for header fields,
   so it needs that check too. The Overseer gave both to this track
   (2026-09-27), on two conditions: the importer's dry run stays at every
   count 0 on the tree, and it is run against the pinned base ROM locally
   before the branch is handed over.

   The trainer lint, new, since the table linter reads no trainer file.
   Errors: a species, form, move, item or nature name that does not exist;
   a level outside 1 to 100; no moves, more than four, or one twice; an IV
   scale outside 0 to 255; an ability slot the species lacks; a gender its
   ratio cannot have; a double battle with one Pokemon. One warning: a
   Choice item, which Ian wants nearly gone (2026-09-26). No move legality
   flags, as Ian asked.

   **The move lists**, three columns, never merged:
   1. Oxide's own at the Pokemon's level, read live from
      `res/pokemon/<species>/data.json` on every request, since the
      learnset cloud job is rewriting the level-up lists: level-up moves at
      or below the level (an earlier stage's too, at its levels), then TM
      and HM, tutor and egg moves. The dex already resolves TM numbers.
   2. Generation IV legal: Showdown's sources marked 4 (Diamond, Pearl,
      Platinum, HeartGold and SoulSilver), with earlier stages' moves
      included as Showdown's validator does. Empty for a species added
      later (Sinistcha has only Generation 9 sources).
   3. Latest-generation legal: the newest generation the species has
      sources in, earlier stages included. Showdown's main file holds
      Scarlet and Violet (9) and Sword and Shield (8), while Brilliant
      Diamond and Shining Pearl are in its `gen8bdsp` mod, which a Sinnoh
      species cut from Scarlet and Violet needs: Bidoof's and Spinda's
      newest main sources are Generation 7. So a Generation 8 list is Sword
      and Shield with BDSP. Legends: Arceus is left out, since it has no TMs
      and learns moves by another system. The Overseer agreed and is
      telling Ian, who may rule otherwise.

   The source is `pokemon-showdown` 0.11.11 from npm (MIT), whose
   `dist/data/learnsets.js` (4.0 MB) and `gen8bdsp` mod (0.6 MB) carry all
   of it. Rather than vendor both files, a generator reads the package once
   and writes the two lists per species to a vendored JSON, with the
   package version and the tarball's hash in a README, as `canon_src/`
   does for the species table.

   **The score**, agreed with the Balance Agent on 2026-09-27. The tool calls
   its `tools/oxide/balance/teamscore.py` and never scores by itself. Both
   calls take the trainer's stem and the unsaved team in the file's own
   shape, place a story fight's variants and tags themselves, and return
   the split and its cap (the balance track's caps in `fights.json`, which
   its tests check against the engine); the cap shows beside the team's
   levels.

   | Call | Where | Time on one core |
   |---|---|---|
   | `teamscore.estimate(stem, data_json)` | every edit | 0.01 to 0.06 s warm, 9 s for the first |
   | `teamscore.score(stem, data_json)` | the "Score it" button | 1 s early in the game, 8 to 20 s late |

   The estimate is the Generation 4 damage formula at the middle roll in
   plain Python (stats, move power and type, STAB, effectiveness, the
   attack items and Choice Scarf; no ability, weather or critical hit). It
   gives safe switch-ins, threat and answers, with safe switch-ins
   corrected by a line fitted to the full scorer and put on the fight
   scale. The line has r² 0.936 over 456 stored fights, and over the 28
   story fights the estimate is 0.26 points off on average and 1.0 at
   worst (Maylene, read too easy); the estimate returns these under
   `"fit"`, and the page shows the number with that margin. `teamscore`
   is at 98ff5bebe on `balance-incremental-b6`, landing with the balance
   track. The server warms the estimate at start, in the background, since
   the first call takes about 9 s. The full score
   runs pinned to one core in the background and returns the plan's scale
   and band, the readings, per-Pokemon rows and the reference hacks' same
   seat. A saved team stales its fight's scores, which the balance track's
   incremental rescore picks up.

   **Build order**, each piece its own commit with its checks, in a new
   suite, `test_trainers.py`, which the gate runs with no change of its
   own, since `integrate.sh` runs every `test_*.py` in the tool's folder:
   1. A read-only tab: the trainer list (name, class, split, cap, the party
      at a glance, filters by split and class) and a trainer page showing
      each member as the game builds it, which `calc_trainers` already does.
   2. The three move lists: the generator, the vendored file and its
      README, and checks on Bidoof's BDSP list, Sinistcha's empty
      Generation IV list and a move only an earlier stage learns.
   3. Editing and saving: the text edits, the round trip over all 928
      files, the trainer lint, the packer check and the divergence file.
   4. The score: the estimate on every edit, and "Score it" in the
      background.
   5. The hidden slot, once the main production agent's engine change
      has merged.

   **Pieces 1 and 2 are done** (2026-09-27, branch `encounter-team-builder`,
   baa9b3007 and 2d8a5ff06): the Trainers tab lists all 928 trainers in
   play order with split and cap, shows a team as the game builds it, and
   gives each member its three move lists. The list's split matches
   `teamscore.resolve`, except that Post has no cap and so no score; 361
   trainers (the dummies and the slots no map fields) have no split at
   all. The vendored lists are `canon_learnsets.json`, from
   `pokemon-showdown` 0.11.11, with their provenance in `canon_src/`.
   `test_trainers` 13/13. Nothing edits yet; piece 3 is next.

   **Pieces 3 to 5 are done** (2026-09-27, the same branch, dfd6f1ba7 and
   88d88d6a0). The tab edits every field Ian listed, removes and adds
   Pokemon, and gives a trainer that lists no moves or items a starting
   set. Each edit is previewed at once (the game's build, the lint, the
   estimate), and Save writes only the changed fields, in the files' own
   list style. The lint, the packer and the divergence registry run as
   planned; the registry is `tools/oxide/trainers_diverged.json`, beside
   the importer, because `sync-docs.sh` refuses a file under `docs/oxide/`
   that it does not mirror. The importer now honours a registered header
   field too, and its dry run stays at every count 0 on the tree; over a
   scratch root holding builder edits it is 0 with the registry, and
   carries Roark's party and Tristan's AI flags back without it. "Score
   it" and the estimate are `teamscore`'s. The hidden slot needed nothing
   more once the engine change and `calc_trainers` had landed (6662712ae):
   the ability menu offers it, and a species without one is a lint
   warning. Every save test runs on a scratch copy. `test_trainers` 25/25,
   `test_m4` 51/51. Still open: Pelipper's and Torkoal's hidden slots are
   Rain Dish and Shell Armor in `res/`, so Ian's staples answer 9 needs
   species data before a trainer's ability 3 gives Drizzle or Drought.
29. **A doc viewer in the tool (Ian, 2026-09-27, through the Overseer).**
   Every document a session points Ian at opens rendered in his browser,
   in the tool's own style, from a link the `doc-links` skill gives:
   `/doc` lists the documents, `/doc/<repo path>` shows one from the main
   checkout on disk, fresh on every request, and `?ref=<branch or
   commit>` shows it at that ref through `git show`. The main checkout,
   not the server's own, because the running server sits in this track's
   worktree, whose branch changes. Links between documents stay in the
   viewer and keep the ref; a link to a code file opens on GitHub.
   Only `docs/` and `.claude/skills/` are served, and nothing writes.
   `docview.py` renders the Markdown with the standard library, and the
   page loads the tool's theme. Done on `encounter-doc-viewer`
   (41c179ece, from `sinistea-split`); `test_docview` 16/16, and all 84
   documents render.
20. **Weather abilities flagged (Ian, 2026-09-26, staples survey).** A
   standing rule: the player never sets, changes or ends weather, so no
   obtainable Pokemon may have Drizzle, Drought, Sand Stream, Snow Warning,
   Sand Spit, Cloud Nine or Air Lock in a regular slot. The main track's
   ability pass is the fix and the species stay in the pool. Until it
   lands, the tool's dex and sources views should flag them. **Done
   2026-09-26:** the dex list (with a Weather filter), the species page, the
   tables' species lists and the scripted pools name the ability. Ten
   species have one: Psyduck, Golduck, Tyranitar, Kyogre, Groudon, Rayquaza,
   Hippopotas, Hippowdon, Snover and Abomasnow. Alolan Ninetales has Snow
   Warning only as its hidden ability, which the rule allows.
   **Lint R18 (2026-09-27)** holds the hidden slot to the same rule where a
   script opens it: no gift, egg or scripted battle that takes
   `FLAG_NEXT_MON_HIDDEN_ABILITY`, and no `GiveHiddenAbility`, may hand over
   a species whose hidden ability sets or cancels weather, at its own stage
   or any it evolves into, since the slot stays through evolution. With the
   natives' hidden abilities imported, eight pick-list species have one:
   Vulpix and Ninetales (Drought), Politoed (Drizzle, so a hidden-ability
   Poliwag fails too), Swablu, Altaria, Lickitung and Lickilicky (Cloud
   Nine), and Alolan Ninetales (Snow Warning). A flag set with no taker
   before the script jumps, and a species the lint cannot read, fail as
   well. Only the test kit sets the flag today, so the tree passes; the one
   Ability Patch stays the only way to such a slot. Seven pick-list species
   still carry a weather ability in a regular slot (Psyduck, Golduck,
   Tyranitar, Hippopotas, Hippowdon, Snover and Abomasnow), for the main
   track's ability pass.
17. **Swarm, Poke Radar and GBA lists emptied (Ian, 2026-09-26, through the
   Overseer).** The three are turned off and never go in a table. This
   track empties the lists in all 186 tables and makes lint fail on any
   species there. It must land in the same merge as the main track's
   engine change, which stops the substitutions; before that, an emptied
   slot would be read as species 0.

## Standing rules

The authoring rules (splits, caps, width, the evolution pass, the no-leak rule
and the whole-game gate) are in the `author-table` skill. These are about the tool
itself.

- The Trainers tab writes `res/trainers/data/` for real. Try a change to
  its save path on a scratch copy first: `trainers.save` takes a folder and
  a registry, and a test server started with `OXIDE_TRAINERS_DIR` and
  `OXIDE_TRAINERS_REGISTRY` reads and writes only those. Every save then
  keeps the importer's dry run at every count 0, because it registers the
  trainer in `tools/oxide/trainers_diverged.json`.
- A save runs the packer in `build/tools/dataproc/`. When `trainerproc.c`
  changes, rebuild it (`ninja -C build -j2 tools/dataproc/trainerproc`); a
  stale one judges by the old rules, and the save's message says so.

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
  rolls exactly as before. The packer fails the build on anything else, since
  the game would loop forever building a party with a 26th nature (item 3).
  How it works and how it was checked are in the archive under M8.
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

**The QA pass before the merge** (2026-09-22,
`docs/oxide/qa-review-2026-09-22-encounter-d4d5.md`; none of it blocked the
merge) is closed but for the importer's report line in item 3. The packer
refused no nature until 2026-09-26 and now refuses all but the 25. The
calculator took the game's chart order for a dual type (**Ian's ruling of
2026-09-22**, `VENDORED.md` patch 9); Crunch into Bronzor had read 42 to 50
against the game's 43 to 51. The dex knows the always-critical effect is done
in C, the licence notices are in (patch 12), and the Z-move twins have a
calculator entry each.

**What is left is Ian's:** one roll in the game against the calculator. In
melonDS, note an attacker's and a defender's level, stats and the damage a
move does. Enter the same two in the calculator, then check the damage falls
in its range.

The visual design (palette B, built and signed off by Ian on 2026-09-22) and the original "Suggested order, and what to cut" are archived in `encounter-tool-build-plan-archive.md`.

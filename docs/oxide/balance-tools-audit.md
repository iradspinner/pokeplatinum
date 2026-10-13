# Balance and scoring tools: audit of `tools/oxide/balance/` (2026-10-13)

**Done the same day.** Ian approved the retirement, and it landed on `oxide` in merge 312060ce0e: the helpers current tools use moved to `calc.py`, `required.py` and `pool.py`, the rest was deleted, and `b6.py` stays as a one-line shim for one driver outside the repo (the tracker has it). `af6c3f6f64` is the last commit with the whole first system. The table below is the audit as it stood before.

Of the 58 modules, 29 should stay as they are, 11 should stay only as libraries for helpers that current tools call, 9 can be retired outright and 9 retired together with their tests (or with their checks inside a shared test). The first scoring system cannot be retired by deleting it. Importing `plgoal3` loads 29 balance modules, six of them first-system (b6, calibrate, metrics, pressure, refpressure, teamscore) and four of them experiments (plgoal2, plines, plstep3, plteam_test). At run time the boss reading calls `b6.placements`, `metrics._placed_filler`, `pressure.run_node` and `fight_weather`, and `teamscore._blob` and `_blob_path`. The OxiDex also still runs the first system live: the team builder computes `teamscore.estimate` on every edit and `teamscore.score` on request, and the Trainers tab shows "The old fight scale" from b6.json, pressure.json and calibrate.json. The OxiDex's own `test_trainers` exercises all of that, and the gate runs it as a blocking check. Today's change made `test_b6` report-only, but it did not touch that path.

Method: a static reference graph over every module in the folder, the OxiDex and the other tools, covering top-level and lazy imports and followed down to the function. I checked it by importing `plgoal3`, `tmcompat`, `learnrewrite` and the OxiDex server and listing what loaded. I added the subprocess and outside-repo callers by hand, and read the commit log since 2026-10-07 and the five status docs. I ran nothing heavy; the only test run was `test_difficulty`, which took 2.3 s and passed 3/3.

## The modules

"Gate" means `tools/oxide/integrate.sh`. "Not in the gate" means no script runs the test; its own track runs it by hand.

| Module | Group | Current caller(s) | Library-only helpers | Decision use since 2026-10-07 | Test and gate status | Recommendation | Confidence |
|---|---|---|---|---|---|---|---|
| b6 | first system | fightsim (split_reading, trainer), plscore.prepare, splits.trainer_rewards (so pool's item census and the scorer's player items), learncheck, learnrewrite, weather_moves, rewards, gauntlet; the OxiDex Trainers tab (split_map, stored scores) | `placements`, `obtainable`, `DEAD_MOVES` for the scorer, census and learnset tools; `OUT`, `load`, `scale_line`, `on_scale`, `band`, `story_scores` for the OxiDex's old fight scale; `run_state` for gauntlet. Move `placements` and `obtainable` to pool or splits later | b6.json was rescored three times on 2026-10-07, and nothing was decided on the numbers. test_b6 held up Roark's accepted team on 2026-10-13, which prompted today's gate change | test_b6 (reported); the OxiDex's test_trainers (blocking) checks b6.json values | keep as library | high |
| buffvariants | first system | none | none | none (buff review, 2026-09-29) | no test | retire | high |
| calibrate | first system | b6's top-level import (so plgoal3 loads it); the OxiDex stored scores (`EXTRA`, `OUT`); plscore.report (`IAN_RATINGS`); rescore | `EXTRA`, `OUT`, `load` for the OxiDex's old fight scale; `IAN_RATINGS` for plscore's report table | calibrate.json rescored 2026-10-07; nothing rests on it | test_b3 B5 checks (reported); test_b6 (reported) | keep as library | medium |
| data | game data | every tool: plgoal3, fightsim, learnset tools, OxiDex trainers and alpha | `fights`, `oxide_trainers`, `fight_trainers`, `raw("kaizo")` (learnstudy) are current; `ref_trainers` serves only the first system and test_b1 | under every decision; unchanged since 2026-09-28 | test_b1 (blocking) | keep | high |
| fightai | scorer | fightsim, perfectline, plplan, so every plgoal3 reading | n/a | AI mirror changed 2026-10-07 (multi-hit, other flags) and 2026-10-12 (Salt Cure); Roark's readings rest on it | test_fightai, test_fightsim, test_plfixes, test_plplan (none in the gate) | keep | high |
| fightfit | first system | ppairs only, which is dead | none | none | no test | retire | high |
| fightsim | scorer | plgoal3 and every scorer module | n/a; its old box mode (`random_box`, `_capture_areas`, which pull in learnwild) serves only plgen and fightfit | Roark's redesign readings, accepted 2026-10-13; the Salt Cure and Eviolite fixes of 2026-10-12 | test_fightsim, test_plfixes (not in the gate) | keep | high |
| gauntlet | game data | rewards (`SECTIONS`, `section_trainers`, `section_reading`), so tmcompat's gate check loads it | `SECTIONS` and `section_trainers` feed trainer-roles.tsv. Its section reading runs on the first system (b6.run_state, teamscore.side, pressure.fight_jobs) and its split average on the B6 scale | the ten sections, approved "as built" on 2026-10-07 | test_b6 (reported) | keep as library | medium |
| hardlove_rom | first system | data.ref_trainers, reached only from metrics, refpressure, levels and test_b1 | none | none | test_b1's Hardlove checks (blocking) | retire with its checks in test_b1 | medium |
| kaizo_docs | game data | learngen, learnwild (the v3 learnset study) | none | none | test_learnstudy (blocking) | retire with its check in test_learnstudy | medium |
| kaizoteams | experiment | plkaizo; plstudy.kaizo_prepare (lazy, the worked examples) | `load_trainers`, `kaizo_records` and kin, for plkaizo only | none | no test | retire | low |
| learncheck | game data | learnrewrite; rewards (so tmcompat's gate check loads it) | n/a | the 2026-10-12 learnset changes passed its rules | test_learncheck, test_learnrewrite (blocking) | keep | high |
| learngen | game data | learnwild, kaizoteams; test_learnstudy's generator check | none | none: the v3 generator gave way to learnrewrite on 2026-10-06 | test_learnstudy (blocking) | retire with its check in test_learnstudy | medium |
| learnrewrite | game data | the learnset generator itself; rewards and tmcompat (`canon_key`) | n/a | wrote the 2026-10-12 lists (Nacli line, Lileep, Sewaddle and Bounsweet, thirteen evolution moves) and the starters' level 5 moves (2026-10-07) | test_learnrewrite (blocking) | keep | high |
| learnstudy | game data | learncheck, learnrewrite, fightsim.play_strength | `kaizo_lists`, `oxide_move`, `strength`, `SPELLING`, `split_of`, `species_constants`; move to learncheck later. Its own report (the study, part 1) is finished | none directly | test_learnstudy (blocking) | keep as library | medium |
| learnwild | game data | learngen, kaizoteams, plkaizo; fightsim's old `random_box` | none for current tools | none | test_learnstudy (blocking) | retire with its checks in test_learnstudy | medium |
| levels | first system | test_b4 only | none | none | test_b4 (reported) | retire with its test | low: the open level-cap design item may want its natural-level curve |
| metrics | first system | b6.placements (so the census, the scorer and the OxiDex), learnstudy, pressure, gauntlet, rescore | `_placed_filler`, `_compact`, `_norm_stats`, `filler_ids`, `late_visits`, `CLOSING`, `STATS`; move to data or splits later | none | test_b2 (reported); test_b1e (blocking, later visits) | keep as library | high |
| pairs | game data | the OxiDex Trainers tab (pair rows), teamscore, b6 | n/a | none | test_b6 (reported); the OxiDex's test_trainers check_pairs (blocking) | keep | high |
| pboxes | scorer | plgoal3 (`context`, `sim`), plniche, plscore | n/a | goal 3's boxes, for Roark and the Kaizo study | test_plgoal3 (not in the gate) | keep | high |
| pdoubles | experiment | plscore.prepare routes tag and double fights to it; plgoal3 reads singles only, so nothing runs it today | none | none | no test | keep (the doubles backlog item starts from it) | low |
| perfectline | scorer | plplan, pldata, plscore, plstep3, plines, plkaizo | n/a. Its turn code is current; its AND-OR search (`perfect`) and its command line serve only plscore's old reader and plkaizo | under every reading | test_fightai, test_plplan, test_plfeat, test_plfixes (not in the gate) | keep | high |
| pldata | scorer | plteam.label (`distill`) on every boss's first box | n/a; its `--sixes` and `--choices` modes are the stage 2 experiments | Roark's readings (labels for the networks) | none direct | keep | high |
| pldifficulty | scorer | plgoal3 (the store); the OxiDex Trainers tab | n/a | Ian's difficulty formula (2026-10-07), shown in the OxiDex | test_difficulty (not in the gate); test_trainers check_difficulty (blocking) | keep | high |
| plfeat | scorer | plplan, plteam, pldata, plnet, plvalue | n/a | Roark's readings (network inputs) | test_plfeat (not in the gate) | keep | high |
| plgen | experiment | plteam.split_strength (lazy), for the blind reading | `trainers`, `trainer_split`; move into plteam later | none | no test | keep as library | medium |
| plgoal2 | experiment | plstudy's top-level import only (examples, comb_roark) | none | none | no test | retire | high |
| plgoal3 | scorer | the boss reading's driver; the Kaizo study's boxes (`roll`, `cut`, `records`, through the Overseer's converters) | n/a | Roark's redesign, accepted 2026-10-13; step 15's first box | test_plgoal3 (not in the gate) | keep | high |
| plines | experiment | plstep3 (top-level import); plscore's old reader (lazy) | none | none | no test | retire | medium |
| plkaizo | experiment | nothing but plstudy's lazy Kaizo path | none | none since 2026-10-07; its Kaizo anchor (2026-10-03 to 10-04) set the boss target of about 80 percent won | no test | retire | low |
| plnet | scorer | plteam.train runs it as a subprocess in `~/venvs/oxide-ml` on every boss's first box | n/a | Roark's readings (the network pair) | none | keep | high |
| plniche | scorer | plgoal3 (`catch_level`, `line_of`, `GOAL3`) | n/a; its own run is learnset checks 2 and 3 | none beyond plgoal3's use | none direct (test_plgoal3 covers its helpers) | keep | medium |
| plplan | scorer | plteam, plstudy, pldata, plgen | n/a | Roark's readings | test_plplan, test_plfixes (not in the gate) | keep | high |
| plpolicy | experiment | none | none | none (the stand-in player failed, 2026-10-02) | no test | retire | high |
| plrescore | experiment | none current; the tracker's Scheduled entry "rescore all 459 fights in the perfect-line store" names it | none | none; its store, perfectline.json, last changed 2026-09-30 | test_pline (not in the gate; the handoff says it passes 1 of 3) | retire with its test, after the Scheduled entry is rechecked | medium |
| plscore | scorer | plgoal3, plteam, plstudy, plniche | n/a. `prepare`, `parse_fight`, `slot_starter`, `with_genders`, `SPLIT_OVERRIDE` are current; `read_fight`, `report` and its command line are the September reader | Roark's readings | test_plfixes (not in the gate) | keep | high |
| plspeed | experiment | none | none | none (PyPy, no gain) | no test | retire | high |
| plstep3 | experiment | plstudy (top-level import), plteam_test, the pldata and plplan command lines; test_plplan, test_plfeat, test_plfixes | `FIGHTS`, `prepare`, `ROARK`, `GARDENIA`, `MARS` as test fixtures; move them to a fixtures module | none | fixtures for three scorer tests (not in the gate) | keep as library | medium |
| plstudy | scorer | plgoal3 (`blind`, `fainted`) | `blind`, `draw`, `pooled`, `read_drawn`, `fainted`; `RES`, `fixed`, `prepare`, `stock` for test_plfixes. Move the blind reading into plteam; the worked examples and the Kaizo path (which pull in plgoal2, plstep3, plteam_test, kaizoteams, plkaizo) go | none since 2026-10-06 | test_plfixes (not in the gate) | keep as library | medium |
| plteam | scorer | plgoal3 (`search`, `full_reading`, `move_pool`, `record`) | n/a | Roark's redesign, accepted 2026-10-13 | test_plfixes, test_plgoal3 (not in the gate) | keep | high |
| plteam_test | experiment | plstudy (top-level import), test_plfixes | `box()`, which reads `~/oxide-trials/three-gym-run` | none | fixture for test_plfixes | keep as library | medium |
| plthreads | scorer | every scorer module that loads numpy | n/a | n/a | none | keep | high |
| plvalue | scorer | plplan.Planner (network value), plnet | n/a | Roark's readings | none | keep | high |
| pool | game data | plgoal3, fightsim, learnset tools, rewards, OxiDex (`caps`, `SPLITS`, `evolution_items_first`) | n/a | TM pass census and the scorer's player items (2026-10-07) | test_b3 check_pool (blocking), test_b1, test_learncheck | keep | high |
| ppairs | experiment | none | none | none | no test | retire | high |
| pressure | first system | fightsim.prepare (`run_node`, `CALC_WEATHER`); fightsim, plscore, plstudy, pdoubles (`fight_weather`); the OxiDex full score and test_trainers through teamscore; gauntlet; rescore | `run_node`, `RUNNER`, `can_evolve`, `fight_weather`, `CALC_WEATHER` for the scorer; move to a calculator module later | Ian approved run_node's Eviolite fix for Roark's reading (2026-10-12); pressure.json rescored 2026-10-07 with nothing decided on it | test_b3 (blocking for the runner, reported for its scores); test_plfixes | keep as library | high |
| refpressure | first system | calibrate's top-level import (so plgoal3 loads it); teamscore.score (the OxiDex full score); rescore | `HACKS`, `load`, `out_path` for teamscore.score | none | test_b3 reference scores (reported) | keep as library | medium |
| required | game data | b6.placements, so the census, the scorer and the OxiDex | n/a | none directly | test_b1e (blocking) | keep | high |
| rescore | first system | the gate's stale-scores line (a warning); test_b3 and test_b6 | none current | three rescores on 2026-10-07; nothing decided on them | test_b3 fingerprint checks and test_b6 freshness (both reported) | retire with its test | medium |
| rewards | game data | its own table and `check` runs; tmcompat imports it (the gate's `tmcompat check` loads it but calls nothing) | `compat` for tmcompat's plan and write | the frozen reward table; Outrage and Dig as second rewards (Ian, 2026-10-07) | none of its own | keep | high |
| run_and_bun | first system | data.ref_trainers only (first system and test_b1) | none | none | test_b1's sheet check (blocking) | retire with its checks in test_b1 | medium |
| shape | first system | rescore, test_b4 | none | shape.json rescored 2026-10-07; nothing rests on it | test_b4 (reported); test_b3 (reported, through rescore) | retire with its test | high |
| splits | game data | every tool; the OxiDex Alpha and Trainers tabs | n/a | TM pass census (2026-10-07) | test_b1 (blocking), test_b3 flag check (blocking), the OxiDex's test_alpha (blocking) | keep | high |
| stones | game data | none (run by hand) | n/a | none; the standing rulings and the balance-rules skill name its census as where stone counts are set | no test | keep | medium |
| teamscore | first system | the OxiDex team builder (estimate on every edit, full score on request, warmed at start), which test_trainers runs in the gate (blocking); fightsim.prepare (`_blob`, `_blob_path`); gauntlet | `_blob`, `_blob_path` for the scorer; move to a calculator module later | teamscore.json refitted 2026-10-07; nothing decided on the estimate | test_b6 estimate fit (reported); test_trainers (blocking) | keep, while the OxiDex shows the estimate | medium |
| tmcompat | game data | the gate (`tmcompat check`, blocking) | n/a | every species' TM list on the new list (2026-10-07) | run directly by the gate. Its import of rewards loads 17 other balance modules for a check that calls none of them; a lazy import would cut that | keep | high |
| weather_moves | game data | learncheck, learnrewrite, rewards (`WEATHER_MOVES`); b6 (lazy) | n/a | none directly | test_weather_moves (not in the gate) | keep | high |
| world | game data | required, so b6.placements | n/a | none directly | test_b1e (blocking) | keep | high |

## The 18 test files

| Test | What it checks | Gate today | Should become |
|---|---|---|---|
| test_b1 | data layers, splits, items, census, TM sources, boss levels, weather, test kit; plus the reference hacks | blocking | keep blocking; move its reference-hack checks (Hardlove, Run and Bun, set counts, milestones, megas) out with hardlove_rom and run_and_bun, which also frees the gate from the donor ROM and about a minute of text decoding |
| test_b1e | required trainers, crossings, later visits | blocking | keep blocking |
| test_b2 | B2 structural metrics | reported | retire |
| test_b3 | calculator runner, engine files, Eviolite, data overrides, player pool, flag numbers (blocking); pressure, B3b and B5 scores and fingerprints (reported) | blocking in part | keep blocking; retire the reported half with rescore and refpressure |
| test_b4 | B4 level curve and the shape grid | reported | retire |
| test_b6 | B6 audit, team builder fit, gauntlet reading | reported | keep reported while the OxiDex runs teamscore; retire it with the old fight scale |
| test_difficulty | the difficulty store and Ian's formula | not run | add to the gate, blocking (2.3 s, 3/3 today) |
| test_fightai | the AI mirror against `trainer_ai.c` at HEAD | not run | add as reported after timing it, since the main track edits the AI |
| test_fightsim | simulator mechanics | not run | add as reported after timing it |
| test_learncheck | the learnset rules | blocking | keep blocking |
| test_learnrewrite | species files are the generator's output | blocking | keep blocking |
| test_learnstudy | Kaizo's lists read, the named-move rule, placement, Kaizo's docs, the v3 generator | blocking | split it: keep check_reading blocking (it guards `kaizo_lists`, which learncheck uses); report the rest until learngen, learnwild and kaizo_docs retire, then drop them. As it stands it can block a landing on a generator nobody runs, as test_b6 did |
| test_plfeat | network features | not run | keep outside the gate (the scoring track runs it) |
| test_plfixes | simulator fixes, 93 checks | not run | keep outside the gate: through plteam_test it reads `~/oxide-trials/three-gym-run`, so a cloud gate cannot run it |
| test_plgoal3 | the driver's boxes, levels and places | not run | keep outside the gate: plgoal3 loads `goal3_fights.py` from `~/oxide-trials/scorer-stage2` |
| test_pline | the perfect-line store | not run | retire with plrescore |
| test_plplan | planner odds and its store | not run | add as reported after timing it |
| test_weather_moves | the weather ruling (no player species learns a weather move) | not run | add to the gate, blocking after timing it; it guards a standing ruling and reads only the tree |

## Not determined, or worth a second look

1. The OxiDex's use of the first system belongs to the encounter track's files (`encounters/trainers.py`, `ui/index.html`, `test_trainers.py`). Whether the old fight scale and the instant estimate stay is Ian's call. If they go, teamscore, calibrate and refpressure move to retire, and b6 and pressure shrink to their helpers.
2. Ian's ruling of 2026-10-07 says "the cheap calculator estimate runs on request, in the background". I could not tell whether that means teamscore's estimate. If it does, the ruling itself keeps teamscore and its chain.
3. Moving the scorer's first-system helpers (and plstudy's blind reading) is a refactor in scoring-track files, which the simulator freeze may cover; it needs the scoring track's or Ian's say-so.
4. The gauntlet rule's "easier side of its split's average" has only one measure today, the B6 scale (`gauntlet.split_average`). Retiring b6's numbers leaves the rule unmeasured until the perfect-line store reads ordinary trainers.
5. plrescore's Scheduled entry predates the 2026-10-07 milestone rule. Under the Scheduled rules it must be rechecked with Ian before plrescore goes.
6. plkaizo and kaizoteams are the only way to re-read Kaizo's bosses on Oxide's boxes, and the boss target of about 80 percent won came from them. Retiring them is safe while git keeps them, but rebuilding would cost a session.
7. Static analysis has limits. I traced by hand the calls it cannot see: subprocesses (plnet; plgoal3 calling itself with `--one`), monkeypatching (plscore sets `fs.BOX_MODE` and `fs.player_moves` at import) and scripts outside the repo. Those scripts are the Kaizo study's tools and the Overseer's Roark scripts in this job's tmp folder, which call `plgoal3.roll`, `cut`, `records`, `plscore.prepare`, `pressure.run_node`, `teamscore._blob_path`, `fightsim.player_items` and `test_fightai.battle`. Test runtimes are unknown apart from test_difficulty's.
8. The balance-rules skill describes how the rescore works (its engine hash, its agreeing second pass). Retiring rescore means updating that paragraph.

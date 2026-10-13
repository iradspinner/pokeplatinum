# The tracker consolidation of 2026-10-13

Ian made `docs/oxide/tracker.md` the one home of open work on 2026-10-13, with the old status homes (`balance-plan.md`, `encounter-tool-build-plan.md`, `trainer-scoring-handoff.md`, `scorer-speed-plan.md`), `alpha-readiness.md` and `qa-plan.md` kept as reference. A helper read those docs, the Kaizo study's notes and the archive's 56 unticked boxes, and checked 142 candidate items against the tree and the log; the Overseer judged each one. Every item classed live is now in the tracker, either already or in its section "Open work by area"; the done and superseded items are listed here with their evidence, and need no action. Ian chose this route (2026-10-13): the Overseer judges, and Ian skims this list.

I read eight sources and checked 142 candidate items against the tree, the git log and `docs/oxide/tracker.md`. I propose 65 as live, 43 as done, 26 as superseded and 8 as unclear. Of the 65 live items, 16 appear nowhere in the tracker, 13 appear only in part, and 36 are already held. Most of the held ones are the tracker archive's unticked boxes, which turn out to be earlier wordings of entries the tracker still carries. The archive's 56 unticked boxes hold nothing the tracker lacks, apart from two small notes (rows T8 and T24). The live items the tracker lacks come mostly from the balance plan, the Kaizo study and the QA plan. Every classification below is a proposal for the Overseer to judge, and "unclear" says why.

| Source | Rows | Live | Done | Superseded | Unclear |
|---|---|---|---|---|---|
| balance-plan.md | 24 | 9 | 7 | 5 | 3 |
| encounter-tool-build-plan.md | 19 | 10 | 7 | 2 | 0 |
| trainer-scoring-handoff.md | 12 | 6 | 2 | 1 | 3 |
| scorer-speed-plan.md | 5 | 1 | 1 | 1 | 2 |
| alpha-readiness.md | 8 | 7 | 1 | 0 | 0 |
| qa-plan.md | 6 | 6 | 0 | 0 | 0 |
| Kaizo study notes (outside the repo) | 12 | 5 | 4 | 3 | 0 |
| tracker-archive.md, unticked boxes | 56 | 21 | 21 | 14 | 0 |
| **Total** | **142** | **65** | **43** | **26** | **8** |

In the "In tracker" column, "partly" means the tracker names the work but not this piece of it, or names it without an owner or trigger.

## 1. balance-plan.md (balance track, stopped 2026-10-07)

| # | Section (line) | Item | Owner, date | In tracker | Evidence | Proposed |
|---|---|---|---|---|---|---|
| B1 | Summary, "Facts the learnset rewrite met" (146-151) | The census owes three corrections at the next rescore: Amity Square unmet, Cynthia's Togepi egg in Fantina's split, fossils from Fantina's split | balance, 2026-10-06 | partly (fossils only, line 126) | `learncheck.py` still patches all three for itself only. Amity Square's header has pointed at its table, with grass, since 506b11dbec (2026-09-26), so that correction rests on a false premise | live (drop the Amity part) |
| B2 | Order of work, design pass 2 (1987-1989) | Replace the Life Orb ball outside Stark Mountain; the main track makes the change | balance, main; Ian 2026-09-27 | no | `events_stark_mountain_outside.json` still has `LOCALID_ITEM_LIFE_ORB`, script 7270, which gives item 270 (Life Orb). No row in `reward-placements.tsv`. Breaks the absolute "no Life Orb for the player" ruling | live |
| B3 | Design pass 2, census correction (1956-1975) | Four kept stones come later than planned (Eterna Moon, Coronet 1F Dawn and Route 213 Water need Surf; Valor Lakefront Sun needs Rock Climb); each goes to Ian case by case at the item pass | balance; Ian 2026-09-29 | no | No stone row in the reward table or `reward-placements.tsv`; nothing in the log | live |
| B4 | Ian's rulings on the Pocket PC (367-373) | The tutor pass: the player's side does not read the world's Draco Meteor or starter-move tutors, "a gap the tutor pass closes" | balance, 2026-09-27 | no | No tutor-pass commit. `learnset-checks.md` puts tutor lists out of scope. New species have empty tutor lists (Scorbunny, Sylveon, Nacli checked) | unclear (no one has said whether a tutor pass is still wanted) |
| B5 | Ian's rulings 2026-09-22 (273-277); design pass 5 (2282-2287, 2396-2398) | The trainer placement pass: more ordinary trainers made unavoidable, toward Ian's "a majority of the game's trainers should be mandatory" | balance; Ian 2026-09-22 and 09-27 | no (only in the standing rulings) | `trainer-roles.tsv`: 40 of 427 required, plus 32 gauntlet members | live |
| B6 | The target (240-244); What B6 found (1152-1155) | The legendary gate: Valor Cavern and Stark Mountain stay empty until the trainer pass lands and is rescored, then the question goes back to Ian | balance, 2026-09-27 | partly (line 141 says they stay off, with no trigger) | The trainer pass landed at step 12 (988ff99ed); step 15's reading is not done | live (after step 15) |
| B7 | Design pass 4 (2268-2269) | Weather on routes and in gyms as a design pass | balance, 2026-09-22 | no | Nothing found in the log or the docs since | unclear (may have been folded into the trainer pass) |
| B8 | Design pass 1 (1807-1810); B4 (1664) | Level-cap redesign from B4's curve; the encounter track then reruns `cli evolve` | balance | yes (line 156) | Not in alpha 1 (Ian, 2026-10-06) | live (after the alpha) |
| B9 | Design pass 3 (1990-2010) | The ability pass: the 228 duplicated second slots, Magic Guard for the Abra line | balance | yes (line 165) | Pelipper's Drizzle and Torkoal's Drought now sit in slot 3; the rest is untouched | live |
| B10 | Where it stood 2026-09-29 (176-178) | Add Glaceon's Ice Scales, with a test-kit entry | balance; Ian 2026-09-30 | yes (line 124) | Glaceon's abilities are Snow Cloak, Snow Cloak and Ice Body | live |
| B11 | Ian's rulings 2026-09-23 (292-295) | A slight nerf to Gardenia's Roserade in the trainer pass | trainer pass, 2026-09-23 | no | Gardenia's whole redesign is in the Scheduled list | superseded (Gardenia's redesign) |
| B12 | Galactic stretch (1264); design pass 5 (2295-2298) | Saturn 2: swap Uxie's Trick Room and Rhyperior's Choice Scarf | trainer pass, 2026-09-25 | no | Uxie now has Stealth Rock, U-turn, Psychic and Thunder Wave; Rhyperior holds a Passho Berry | done |
| B13 | Galactic stretch (1306-1312) | Roster work for Cyrus 2 and for Mars and Jupiter at Spear Pillar | trainer pass, 2026-09-26 | no | Replaced by the comb's teams at step 12 (988ff99ed) | done |
| B14 | Design pass 5 (2282-2283) | Take the Choice items off the bosses | trainer pass; Ian 2026-09-25 | partly | No boss before the post-game holds one, except Wake (two). Wake keeps today's team for alpha 1, and his rework is scheduled after it | done (Wake excepted) |
| B15 | Part 3 (2263-2267) | For Ian: level-1 order, exclusive delays, a move for Fletchinder | balance, 2026-09-27 | no | Learnsets moved to check and verify on 2026-10-06; the rewrite landed at 085f72211 | superseded |
| B16 | Order of work, B1c (1613) | Read Odyssey from its ROM | balance, 2026-09-22 | no | No work since. The perfect-line scorer replaced the reference-hack measure | superseded |
| B17 | B5 (1718-1719) | B5 cannot score the double battle | balance | yes (backlog, doubles) | Now the scoring track's doubles planner | superseded |
| B18 | Last paragraph (2487-2490) | Fix the packer accepting `NATURE_COUNT` before the trainer pass uses natures | encounter | no | The packer refuses anything but the 25 natures (encounter plan, item 3) | done |
| B19 | Design pass 2 (1952-1953) | The Pixie Plate takes one fixed find | item pass | no | `reward-placements.tsv` row 158: Beauty Nicola, Route 222 | done |
| B20 | Design pass 2 (1881-1941) | Close the Underground, remove both bulk stone sets, make the Old Amber ball an Everstone | main; Ian 2026-09-27 | no | 9224f5cca4, b00b029b57 | done |
| B21 | Design pass 2 (1977-1985) | The census counts an after-win reward at the trainer's split | balance, 2026-09-29 | no | 41fd1f6019, ee0ddb3911 | done |
| B22 | Summary, where the track stopped (39-44) | The starter data leaves 179 scores stale until step 15's reading | balance, 2026-10-07 | partly (step 15) | Step 15 stopped on 2026-10-07 | live (inside step 15) |
| B23 | Tracker line 155; unlanded branches | `balance-fight-sim`, `balance-sim-example`, `balance-boxmodel` (8 commits, a WIP box-model rescore), `wip-balance-b3b`, `balance-learngen-v2`, `cloud/balance-learnset-pass`, `balance-learnset-review` are unmerged | balance | partly (the first two) | None is ancestor to `oxide`; the scoring track and the landed rewrite cover their purposes | superseded (retire the branches) |
| B24 | Design pass 2 (1825-1826) | When a confusion cure is first in reach decides how Swagger plays; Gardenia has no Persim Berry | item pass | no | Nothing found | unclear (an observation, with no action named) |

## 2. encounter-tool-build-plan.md (encounter track, stopped about 2026-10-07)

| # | Section (line) | Item | Owner, date | In tracker | Evidence | Proposed |
|---|---|---|---|---|---|---|
| E1 | What is open, 1 (157-159); "Maylene's cap" (1502-1513) | Maylene's tables are designed at 38; rerun `cli evolve` once the final caps land | encounter, 2026-09-22 | yes (line 7) | The engine's `sLevelCaps` plays 39, and the cap redesign is not in alpha 1, so the wait now runs past the alpha | live (could run at 39 now) |
| E2 | 2 (160); M8 (1533) | Ian's one damage roll against the calculator | Ian | yes (checklist, line 197) | Still unticked | live |
| E3 | 5 (193) | Which trainer Pokemon get a named nature | Ian, Phase 5 | no | Ian ruled on 2026-10-12 that every enemy Pokemon has its own nature, and the comb sets natures | superseded |
| E4 | 7 (226-240) | The Amity Square and Snowpoint City casts are drafts for Ian to change | Ian, 2026-09-25 | no | Unchanged since | live (low) |
| E5 | 11 (280-292) | The eight honey tree tables are a first draft for Ian; shake a tree at one badge and at five | Ian, 2026-09-26 | partly (the shake only, checklist 485 and 581) | Unticked | live |
| E6 | 13 (301-312) | The Box sim's line ratings in `values.json` are a first draft for Ian | Ian | yes (line 7) | No change recorded | live |
| E7 | 45 (1239-1254) | The water biome draft goes to Ian as one question; water tables re-authored after the zone pass | Ian, encounter, 2026-09-29 | yes (lines 55, 122) | 854 lint warnings stand | live |
| E8 | 46 (1323-1330) | Zone-by-zone pass proposals: starter homes, Froakie's 1%, late new lines, Fairy in Wake's and Byron's splits, Starly evolving in the wild | encounter with Ian | yes (lines 14, 122) | Not started | live |
| E9 | 50 (1368-1376) | The regional dex order for 51 lines | Ian, 2026-09-30 | yes (line 53) | Waiting | live |
| E10 | 51 (1377-1379) | Alpha tab check 7: Ian looks at the page on today's data | Ian | partly (line 14 says the layout notes are being worked) | The layout landed (212e3675ea) | live |
| E11 | 25 (542-560) | Thorton's prize capture and Argenta's item reward wait on the Frontier Brains | Ian builds the teams | yes (lines 142-145) | No Brain team yet | live |
| E12 | 15 and 16 (337-340) | The Route 226 trade becomes Meloetta | encounter, main | no | Meloetta landed; the Meister's trade gives it | done |
| E13 | 18 (386-388) | Trimming the 75 to 85 tier waits on the wanted list | Ian | no | The trim was done once the wanted list came (same item) | done |
| E14 | 19 (433-434) | The balance rescore after the calculator learned element 5's abilities | balance | no | Several full rescores since | done |
| E15 | 28 (793-795) | Pelipper's and Torkoal's hidden slots must give Drizzle and Drought | species data | no | Slot 3 holds Drizzle and Drought in `res/` | done |
| E16 | 32 (871-882) | Ten cap candidates each need a table change | encounter, 2026-09-27 | no | 1caf28aba6, "ten swaps clear the cap candidates" | done (the entry is stale) |
| E17 | 6 (220-223) | The gate could lint R12 on the working tree | Overseer | no | `integrate.sh` line 470 lints with R12 included | done |
| E18 | 8 (255) | Retire the battle zone plan's Metagross line | Overseer | no | `battle-zone-plan.md` line 114 already reads closed | done |
| E19 | Milestones (1479) | Full species placement in the generator | encounter | no | "Deferred, possibly for good" | superseded |

## 3. trainer-scoring-handoff.md (scoring track, stopped 2026-10-07)

| # | Section (line) | Item | Owner, date | In tracker | Evidence | Proposed |
|---|---|---|---|---|---|---|
| S1 | Summary (22-77) | Restart goal 3's milestone reading (step 15) with the given command, including Lucas and Dawn 1's failed box; then run `plgoal3 --store` | scoring, 2026-10-07 | yes (Scheduled, line 27; readiness step 15) | 1 of 117 boxes done; stopped at 18:22 on 2026-10-07 (0f21be7b6a). The tracker still says the agent is running | live |
| S2 | Summary (52-53, 147) | The 41 Ace Trainers are not read at this milestone | scoring; Ian 2026-10-07 | no | Deferred by Ian | live (next milestone) |
| S3 | Summary (84-85, 148) | A boss team that lands after the QA ROM is re-read before the alpha ROM is fixed | scoring | partly (readiness step 16) | Roark's redesign landed on 2026-10-13 and was read at 86 percent won (d537eaea74); Gardenia's redesign would be next | live |
| S4 | Summary (18-20, 149-151) | The doubles and tag planner, for about 60 fights | scoring; Ian 2026-10-06 | yes (backlog, line 195) | Not started | live (unscheduled) |
| S5 | Where it stands (248-250); Ian's answers 2026-10-01 | Rescore the 459 fights in the perfect-line store | scoring | yes (Scheduled, line 33) | Its trigger (the comb applied) was met at step 12, but Ian's rule of 2026-10-07 limits full readings to milestones, and goal 3 now does that job | unclear (likely superseded by the milestone reading) |
| S6 | Moves the simulator ignored (1920-1926) | Simulate Camouflage before goal 3 reads Barry 3 | scoring, 2026-10-03 | yes (Scheduled, line 31) | No trainer file uses `MOVE_CAMOUFLAGE` now, which meets the entry's own "Unneeded if" | superseded |
| S7 | Team search (1696-1701) | Held items are not searched; the finalists might try the box's held items. Late bosses read slightly hard | scoring, 2026-10-02 | no | Proposal only; the simulator is frozen except for fixes Ian approves | unclear |
| S8 | fightai audit (626-635); 1925 | Mechanics the simulator leaves out: double-battle AI partners and switch rules, Me First, Copycat, Judgment's plate, Gravity, Foresight, Embargo, Sleep Talk's choice, Baton Pass, per-hit contact effects | scoring | no | Unchanged; the freeze applies | live (parked) |
| S9 | Where it stands (252-253) | `perfectline_results/kaizo.json` was never committed; rerun `plkaizo.py` | scoring | no | Housekeeping only | unclear |
| S10 | Kaizo comb of Roark's split (2348-2360) | Youngsters Darius and Jonathon were read without the gym's sand; they wait for the full reading | scoring, 2026-10-06 | no | Not re-read | live (next full reading) |
| S11 | Ian's answers 2026-10-03 (1949-1950) | Read Jupiter 1 again once Attract works | scoring | no | Goal 2 was re-read on the fixed simulator ("Goal 2 read again") | done |
| S12 | Kaizo comb (2316-2337) | Adjust the blind pool for a shared weakness | Ian | no | Ian kept the rule on 2026-10-06 | done |

## 4. scorer-speed-plan.md

| # | Section (line) | Item | Owner, date | In tracker | Evidence | Proposed |
|---|---|---|---|---|---|---|
| P1 | Goal (3-6, 19-20) | Goal 4: a whole-game reading in hours, with boxes and the stress test | scoring; Ian 2026-10-02 | no (memory only) | Goal 3 reuses one network pair per boss (3f7e4ebeba); goal 4 not started | live (long term) |
| P2 | Levers (59) | Stage 3: the simulator and AI in a compiled language | scoring | no | "In reserve" | unclear (parked) |
| P3 | Levers (61); 134-160 | A cheaper opponent AI with identical results | scoring; Ian's brainstorm 2026-10-02 | no | "Not yet work" | unclear (idea) |
| P4 | Stage 2 (214-221) | Labelled positions for every boss | scoring | no | Built into goal 3's driver | done |
| P5 | Levers (60) | Stop a fight's reading early once its numbers settle | scoring | no | Ian set a fixed 100 fights | superseded |

## 5. alpha-readiness.md

| # | Step (line) | Item | Owner, date | In tracker | Evidence | Proposed |
|---|---|---|---|---|---|---|
| A1 | Step 14 (28) | Ian's QA pass from the checklist | Ian | partly (line 18) | Status cell empty | live |
| A2 | Step 15 (29) | The milestone reading | scoring | yes | Same as S1 | live |
| A3 | Step 16 (32) | QA's hotfixes, then the alpha 1 ROM | Overseer, tracks | partly (line 175 points here) | Not started | live |
| A4 | Step 11 (25) | Ian swaps in the `beacon-moves` melonDS build; the recorder's live check | Ian | yes (checklist, line 78) | Unticked | live |
| A5 | Status line (8); step 12 (26) | The comb's 271 ordinary trainers (task 4) go in at "the next comb landing" | Overseer, balance | partly (Scheduled, line 28, with no trigger) | 272 comb files differ from `res/` (these 271 and Roark); the Balance Agent has stopped | live |
| A6 | Step 12 (26) | Ian chooses any retunes from step 15's readings | Ian | no | Waits on step 15 | live |
| A7 | Step 3 (17) | The learnset rewrite's named cases, staple coverage (question 4) and check 8's late shortfall, left for after the alpha | balance, Ian; 2026-10-06 | no | `learnset-rewrite.md`, action items 1 and 2 | live (after the alpha) |
| A8 | Step 13 (27) | The status cell still says "under way 2026-10-07" | Overseer | no | The status line says steps 1 to 13 are done | done (a doc tidy) |

## 6. qa-plan.md

| # | Section (line) | Item | Owner, date | In tracker | Evidence | Proposed |
|---|---|---|---|---|---|---|
| Q1 | 1 (5-18) | The eight test-kit checks of the week's systems | Ian | partly (line 18) | Unticked | live |
| Q2 | 2 (20-22) | The run, with the recorder and the Alpha tab | Ian | partly | Not started | live |
| Q3 | 3 (26) | The older move sets 23 to 70; the Overseer offered to cut the list to moves a trainer or player list carries first | Overseer | no | Not done | live |
| Q4 | 3 (27) | Rewrite the live checks that name replaced teams before the joint stub session | Overseer | no | Volkner's Rotom is form 0 now (no Rotom-Mow, checklist 727). Zackary's Castform is level 24, not 15 (469). Gardenia's team has no Cherrim (579), a fourth stale check the plan does not name. Jackson's Wormadam-Trash still stands (616) | live |
| Q5 | 3 (28) | Section 5's checks after the League | Ian | yes (checklist) | End of a run | live (deferred) |
| Q6 | 3 (29) | The out-of-date HM check | Overseer | no | Checklist line 272 still says "An HM taught from the case stays" | live |

## 7. The Kaizo study (`~/oxide-trials/kaizo-teams/out/`)

| # | Source (line) | Item | Owner, date | In tracker | Evidence | Proposed |
|---|---|---|---|---|---|---|
| K1 | resume-notes "First job on restart" (12-22) | Mirror the accepted Roark in `comb/`: switch `comb_roark.py` to the accepted spec, rebuild, ask the Overseer to diff | study; Overseer 2026-10-13 | partly (line 117) | `comb/leader_roark.json` differs from `res/` | live |
| K2 | resume-notes (83, 101) | Gardenia's redesign, in checked stages, on goal 3's boxes | study; Ian 2026-10-12 | yes (Scheduled, line 29) | Not started | live |
| K3 | task4-summary "Decisions for Ian" (35-44) | Six decisions, each recommended "accept": ordinary trainers past the faint band, Rocco rebuilt, Wake's ability weather, Brennan's Shedinja and Vincent's rain, HQ's two-Pokemon grunts, Somnu read as a boss with Tyche's and Hermes's Explosions removed | Ian, 2026-10-07 | no | No answers recorded | live |
| K4 | retune README "Weather from abilities" (19-30) | Three items do nothing under permanent ability weather: Flint's Torkoal's Heat Rock, Moira's Abomasnow's Icy Rock (Mt. Coronet), Jonah's Hippowdon's Smooth Rock | Ian (no retunes without him) | no | All three are in `res/trainers/data/` | live |
| K5 | retune README (1-17) | Unapproved retune candidates: Cynthia, Maylene, Flint, Lucian, Aaron, Bertha, Barry 3, Saturn 1, Argo, Barry 6, Aces Jose, Saul and Mariah | Ian, after step 15 | no | Kept for him; none applied | live (after step 15) |
| K6 | task4-summary (54-60); resume-notes (129) | The study's simulator misses Eject Button, Red Card, Sticky Web, forms and more | study | no | Ian's rule: only when a team leaning on one is materially in question | superseded |
| K7 | notes-for-later (7-8) | Add Dark Void to Darkrai's egg list for Somnu | balance; Ian 2026-10-06 | no | Darkrai's egg list holds Dark Void | done |
| K8 | notes-for-later (1-6) | Build the Game Corner challenger | study, main | no | `game_corner_challenger.json`, placed at step 10 | done |
| K9 | notes-for-later (9) | The legality sweep, on hold | study | no | Redone on 2026-10-07 (`legality-hold.md`) | done |
| K10 | resume-notes (56) | Ian's pick between Roark versions (a) and (b) | Ian | no | He took the uncut team with Recover (2026-10-13) | superseded |
| K11 | notes-for-later (10-16) | The early blind readings and the calibration predate the tie fix | study | no | Ian's rule of 2026-10-07: no re-read unless the change is material | superseded |
| K12 | resume-notes (197-238) | The simulator patch for modern teams, Fake Out first | study | no | "Done since" (line 110) | done |

## 8. tracker-archive.md, the 56 unticked boxes

The archive keeps blocks verbatim, so most unticked boxes are earlier wordings. "Live, held" means the tracker carries the current entry; the archive box itself needs no action.

| # | Line | Item | In tracker | Evidence | Proposed |
|---|---|---|---|---|---|
| T1 | 114 | The 21 natives whose sheet and base ROM stats disagree | yes (61) | Unchanged | live, held |
| T2 | 171 | The base ROM's custom overworld sprites | no | Done 2026-09-26 (tracker line 71) | done |
| T3 | 173 | Vs. Seeker PC, hue shift, the two-byte change | no | All ported or ruled out (tracker line 73) | done |
| T4 | 180 | Element 8, wording of 2026-10-02 | yes (109) | Later wording | superseded |
| T5 | 189 | Expert routines for the new moves | no | Merged at 170b5473a (tracker line 105) | done |
| T6 | 209 | Fairy's two art pieces | yes (79) | Unchanged | live, held |
| T7 | 221 | Element 3 | yes (80) | | live, held |
| T8 | 230 | What element 3 left short | yes (81) | TM lists are now written (step 8); new species' tutor lists are still empty and most egg lists too, so the tracker line is half stale | live, held |
| T9 | 237 | The form fix's emulator check | yes (82, checklist) | | live, held |
| T10 | 239 | Re-run element 3's check after each element | yes (84) | | live, held |
| T11 | 240 | Element 4 | yes (85) | | live, held |
| T12 | 258 | The new battle effect scripts | yes (86) | | live, held |
| T13 | 291 | The 2026-09-22 QA leftovers (`RANGE_ALL`, computed powers, `.shared`, the TV move) | no | `battle_lib.c` handles `RANGE_ALL`; 448000f759 removed `.shared`; powers closed 2026-09-29; TV archived 2026-10-12 | done |
| T14 | 294 | The widened learnset's emulator test | yes (93) | | live, held |
| T15 | 297 | Element 5 | yes (94) | | live, held |
| T16 | 299 | Element 6 | yes (98) | | live, held |
| T17 | 303 | Keep AI fixes and changes separate | yes (103) | | live, held |
| T18 | 306 | Teach the AI the new moves, abilities and held items | partly (101, Ian's item 3) | The Expert and AI flags passes did the moves; the held items wait on Ian | live, held |
| T19 | 319 | Element 7 | no | Done (tracker line 108) | done |
| T20 | 320 | Element 8, first wording (the 17 dead trade entries) | yes (109) | The trade strip landed (`cloud/element8-batch1`) | superseded |
| T21 | 366 | The QA leftovers, second wording | no | As T13 | done |
| T22 | 371 | The base ROM's last arm9 changes | no | Merged (tracker line 73) | done |
| T23 | 384 | Field moves on the badge alone | yes (checklist) | Landed fe21d95cb; only Ian's check is left | done |
| T24 | 385 | 30 PC boxes | yes (checklist) | Landed; one vanilla oddity (the dial's thumbnail cache flush) was "reported, not fixed" and is in no tracker line | done (the oddity is unclear) |
| T25 | 393 | Kaizo study, wording of 2026-10-02 | yes (118) | | superseded |
| T26 | 394 | Balance analysis, the scorer rebuild wording | yes (155) | | superseded |
| T27 | 395 | The Kaizo comparison | yes (149) | | superseded |
| T28 | 396 | The player never controls weather | yes (139) | Landed aa3bbc3356 | done |
| T29 | 403 | Balance analysis, first wording | yes (155) | | superseded |
| T30 | 405 | Level-cap split design | yes (156) | | live, held |
| T31 | 406 | The TM pass | yes (157) | Landed at 787c581c8, yet still open in the tracker | done |
| T32 | 407 | The ability pass | yes (165) | | live, held |
| T33 | 408 | Encounter design decisions (the hidden-ability flag) | yes (166) | | live, held |
| T34 | 409 | Verity Lakefront as a capture area | no | 506b11dbec | done |
| T35 | 410 | The starter's own met location | no | "Rowan's Briefcase" (encounter plan, item 6) | done |
| T36 | 411 | Route 211 east as a delay | no | Authored: Kirlia and Dartrix there | done |
| T37 | 412 | Delete the four off-list fossils | no | b00b029b57, 9224f5cca4 | done |
| T38 | 413 | Floette's flower forms | yes (168) | | live, held |
| T39 | 414 | A PKHeX build (optional) | yes (169) | | live, held |
| T40 | 433 | The Battle Zone, a wording of 2026-09-26 | yes (131) | | superseded |
| T41 | 437 | Balance analysis, 2026-09-23 (B3b parked on `wip-balance-b3b`) | yes (155) | B3b finished 2026-09-25 | superseded |
| T42 | 455 | The Battle Zone (Heatran as a pool draw) | yes (131) | Stark Mountain's room is empty (Ian, 2026-09-27) | superseded |
| T43 | 479 | Verity Lakefront, a duplicate | no | 506b11dbec | done |
| T44 | 480 | Amity Square as a capture area | no | 506b11dbec. This contradicts the tracker backlog (line 206) | done |
| T45 | 529 | The score is rebuilt | no | The perfect-line planner (scoring track) | done |
| T46 | 531 | The Barry split | yes (153) | The engine caps at 71; the Fight Area aces are 68 and 69 | done |
| T47 | 559 | Kaizo study, 2026-10-03 wording | yes (118) | | superseded |
| T48 | 563 | The Kaizo learnset pattern study | yes (150) | Learnsets by check and verify, 2026-10-06 | superseded |
| T49 | 564 | The generator's 652-species proposal | yes (150) | Same | superseded |
| T50 | 568 | Kaizo study, 2026-10-06 wording | yes (118) | | superseded |
| T51 | 572 | Gauntlets in game | yes (120) | Landed with step 10 (787c581c8), yet still open in the tracker | done |
| T52 | 574 | Move reworks | yes (158) | Archived on 2026-10-07 once built; the box was never ticked | done |
| T53 | 583 | The UNLOCK FPS ALWAYS crash | no | 60 fps outside battle was dropped (917424237) | superseded |
| T54 | 585 | The box deposit hang | yes (186) | `main-box-hang` is merged; only Ian's check is left | live, held |
| T55 | 587 | A ported element visibly works (Fairy) | yes (188) | | live, held |
| T56 | 590 | The Poketch and Pokedex on a Fairy Pokemon | yes (189) | | live, held |

## Tracker entries these checks touched

These are not part of the counts, but the Overseer may want them while consolidating.

- Done but still open in the tracker: the TM pass (157), gauntlets in game (120), the move reworks (158) and the rampage moves (159, now one-turn in `res/moves`). Sylveon is reachable (160): Eevee learns Charm at 27, and TM41 Charm is a Game Corner prize. Togepi has attacks (161): Fairy Wind at 1, Dazzling Gleam at 2 and Magical Leaf at 4. Route 207's trainers are in Fantina's split (163): `trainer-roles.tsv` places all six there.
- Still live: the Jubilife grunts sit in Roark's split in `trainer-roles.tsv` (162). The PP ruling is unapplied (164): Growl, String Shot and Cotton Spore are at 40, and Defog at 15. Grimer, Muk and Bibarel are not placed (122). Delibird is still only in late tables (167).
- Lapsed: the Camouflage entry in the Scheduled list (S6). The Amity Square backlog line (206) rests on a false premise (T44). The perfect-line rescore's trigger is met but conflicts with the milestone rule (S5). "Who is on what" (lines 10-19) describes sessions that stopped around 2026-10-07.

## Found while checking, in no source

- The Celestic Town northwest house gives a Choice Specs on a morning visit (`scripts_celestic_town_northwest_house.s`, line 44), which breaks the absolute ruling that the player never gets a Choice item. The Battle Points shop's Choice Band and Scarf are in the backlog already.
- 48 trainer teams in `res/` (rematches left out) give two members the same held item, against Ian's ruling of 2026-10-12. So do 35 of the 271 combed teams still waiting to land. The ruling is a design preference, not a gate check.

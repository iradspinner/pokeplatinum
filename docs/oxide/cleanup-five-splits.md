# The first five splits: a cleanup check

Ian asked on 2026-10-31 for a short pause, with cheap checks only, to make sure the work on Roark's, Gardenia's, Fantina's, Maylene's and Wake's splits (caps 16, 26, 33, 39 and 44) is clean. Six checks were run on the branch `overseer-cleanup-five`. No scorer ran, and the simulator, its AI and the scorer are unchanged. No team Ian built or has seen was changed; each finding on one is a question below.

## Summary

The helper-built teams of Gardenia's to Wake's splits are clean, and the tables, the OxiDex's caps and the checklist are done. What is left is on Ian's own teams, the bosses and Roark's split, which was left as it was.

| Check | Now | Fixed here | Waits on Ian |
|---|---|---|---|
| 1. Every trainer clean | Fails on Ian's teams, the bosses and Roark's split | Four Roark's split teams: one move listed twice, two repeated natures, one repeated item | Questions 2 to 4, 9 |
| 2. Levels follow the soft caps | Passes for helper-built teams; mini-boss aces pass | Twelve Wake's split teams one level down, so Barry 4's stretch tops at 41 | Questions 2, 5 to 8 |
| 3. Mandatory fights | Roark 8, Gardenia 12, Fantina 10, Maylene 11, Wake 10, none changed since its pass | Nothing to fix | Question 1 |
| 4. Role and reward tables regenerated | Passes | Both tables whole; the Jubilife grunts' split corrected | Nothing |
| 5. The OxiDex's honour caps | Passes | The over-cap flag reads each mini-boss's cap | Nothing |
| 6. In-game checklist for the five splits | Done | A new section, 28 checks in play order | Playing it, about six hours |

Ian's questions:

1. Roark's split has 8 mandatory fights, the number he asked for on 2026-10-29, under the 10 to 15 that holds elsewhere. Does 8 stand?
2. Roark's split was left as it is, and it shows. In its 16 ordinary and gym teams, 44 of 60 members hold no item and 47 name no nature, against his rule that every member holds its own item and has its own nature. 8 of the 16 top at 15, one under the cap of 16, where one under should be rare. Should Roark's split get the same pass the other four had, or stay as it is?
3. Barry 2 on Route 203 gives an Oran Berry to three members in all three versions, and his Piplup version has two Adamant members. Change them?
4. Beauty Devon's two members on Route 214 are both Gentle. Change one?
5. Krystal's Dragonair is at 42 in Barry 4's stretch, at its cap, where an ordinary trainer never should be. Lower her by one, or keep her as the hard gate he chose?
6. Collector Jamal tops at 41 (his Delibird) in the same stretch. His Noctowl's Tailwind is on no list for it, and none of his four members names a nature. Leave him as he is, as he said for the Wake pass?
7. Darach and Caitlin, at 44, can be fought before Barry 4. Pastoria lifts Route 212's blockade when its map loads, and Barry's trigger is one tile at the gym door, so Route 212 North and the mansion open as soon as the player reaches Pastoria. Keep them at 44 (an optional boss over the stretch's cap), gate them behind Barry 4, or lower them?
8. Behind Darach, Maid Clare and Lady Celeste are both at 42 and the other maids at 40 and 41. Keep them?
9. Fourteen moves on the Galactic fights and Lucas and Dawn 1 are on no list for their species at their levels (the table under check 1). Should they go on their lines' first-stage egg lists, under his ruling of 2026-10-29, or should their teams change?

Next steps:

| Step | Who | Time |
|---|---|---|
| Land `overseer-cleanup-five` with `merge-branch.sh`, then `sync-docs.sh` on `oxide` | the Overseer | 30 minutes |
| Answer questions 1 to 9 | Ian | 15 minutes |
| Apply his answers (egg lists, natures, levels, Roark's split if he wants it) | the Overseer | 1 to 3 hours, the most for Roark's split |
| Play the checklist's new section, "The first five splits, in play order" | Ian | about six hours, in pieces |

Unverified: nothing here was seen in game, and no fight was read by the scorer. The Barry 4 stretch is read from the field model, not walked.

## Check 1: every trainer clean

Every trainer the OxiDex tags in the five splits was read (256 files, Dahlia's `dummy_007` and Darach's `dummy_008` among them). For each: the trainer lint; the Kaizo checker (`oxide.py check <cap>`, with `OXIDE_OLD_RES` at the export of 5c62989651's `res/`, as the boss checks used it); the OxiDex's own lists (`learnsets.oxide_list` at the member's level); a held item and a named nature on every member, with no repeat in a team; no one-hit KO move; and no `NATURE_COUNT`.

Where the two checkers disagree, the OxiDex alone flags a move cut in the TM pass, which stays in the trainer palette (Ian, 2026-10-07): the tracker already lists that gap. Those are legal and not listed below. The checker's notes on a member under its evolution level are left out too, since Ian allows one "not egregiously early".

Fixed, on teams the Kaizo comb built for Roark's split, each through `trainers.save` (lint and packer clean):

| Trainer | Was | Now |
|---|---|---|
| Picnicker Diana | Skitty listed Baby-Doll Eyes twice, which the lint refuses | the second copy is no move |
| Worker Mason | Makuhita and Larvitar both Adamant | Larvitar Brave |
| Youngster Tristan | Sentret and Starly both Jolly | Sentret Hasty |
| Youngster Michael | Paras and Oddish both held an Oran Berry | Oddish holds a Cheri Berry |

Each new nature keeps the stat the old one raised.

Moves on no list at the member's level, by both checkers (question 9):

| Trainer | Member | Move | Where its line has it |
|---|---|---|---|
| Mars 1 | Liepard 18 | Faint Attack | nowhere |
| Mars 1 | Torracat 19 | Flame Wheel | nowhere |
| Somnu 1 (`galactic_grunt_valley_windworks_3`) | Gastly 17 | Nightmare, Sludge | nowhere |
| Somnu 1 | Munchlax 17 | Yawn, Body Slam, Crunch | nowhere |
| Jupiter 1 | Lanturn 26 | Discharge | Lanturn at 40 |
| Jupiter 1 | Galarian Weezing 28 | Strange Steam, Toxic Spikes | nowhere |
| Eterna building 3F (`galactic_grunt_team_galactic_eterna_building_3f`) | Snover 25 | Ice Shard | Snover at 26 |
| the same | Xatu 25 | Future Sight, Air Slash | nowhere |
| the same | Galarian Mr. Mime 25 | Freeze-Dry, Future Sight | nowhere |
| the same | Lunatone 25 | Future Sight, Icy Wind | nowhere |
| the same | Kadabra 26 | Future Sight, Icy Wind | Kadabra's Future Sight at 42 |
| Lucas and Dawn 1, the Turtwig versions (`dummy_788`, `dummy_791`) | Turtwig 9 | Absorb | nowhere |
| Collector Jamal (Ian's) | Noctowl 38 | Tailwind | nowhere |

Each was legal when built, as far as the passes record: the learnset rewrite and the move cuts moved them since. Snover's Ice Shard is the case Ian's Gardenia ruling allows (a move learned just after the split). Gardenia's Exeggutor's Egg Bomb at 24, which it learns at 27, is that ruling's own example.

Repeats on teams Ian built or a boss (questions 3 and 4): Barry 2's three versions (three Oran Berries; two Adamant in the Piplup one) and Beauty Devon (two Gentle).

Members with no item and no nature: Roark's split (question 2); Barry 1's and Lucas and Dawn 1's one-member teams; Ruin Maniac Ronald (no nature on all five) and Collector Jamal (none on four), both Ian's. Barry 1 does not count for deaths (Ian, 2026-10-02).

Not in the five splits' work, though the OxiDex tags them there:

- The Restaurant's nine daily doubles, vanilla teams at 24 to 31 that wait for a later pass (the Wake split's ruling). Most members hold nothing and name no nature, Pokefan Meredith repeats a Sitrus Berry, and Gentleman Leonardo's Chatot has Mimic and Fury Attack, which it cannot learn.
- The Surf trainers, met only in Byron's split: Route 213's four Swimmers and Sailor Paul, Fisherman Cody on Route 208, and Tubers Mariel and Trenton on Route 219. Sailor Paul's Kingler has Guillotine and Tuber Trenton's Dewgong Sheer Cold, one-hit KO moves that the Scheduled list takes off as each split is worked; four carry a move on no list. The census places them in Wake's split only because their aces (43 and 44) sit over their maps' caps.
- The gym leaders' rematches (post-game; three Choice items among them), the Diamond and Pearl gym rooms' Camper Drew and Picnicker Cheyenne (connected to nothing), and the partners Cheryl and Mira.

## Check 2: the levels and the soft caps

No ordinary or gym trainer in the five splits is over its split's cap. At the cap or one under:

| Split | Ordinary and gym teams | At the cap | One under |
|---|---:|---:|---:|
| Roark (16) | 16 | 0 | 8 |
| Gardenia (26) | 39 | 0 | 0 |
| Fantina (33) | 44 | 0 | 0 |
| Maylene (39) | 37 | 0 | 1, Black Belt Jeffery in the gym |
| Wake (44), the gym | 6 | 0 | 1, Sailor Samson, the last guard, as the Wake pass set |

Jubilife's two grunts first read as at Roark's cap. They appear only once Roark is beaten (his gym's script clears their hide flag), so they are Gardenia's split's, as the early mandatory-fights pass counted them; the census now places them there. The Surf trainers above read at Wake's cap only by that tagging.

Each climb doc's table (`level-climb-gardenia.md`, `level-climb-fantina.md`, `level-climb-maylene.md` and `wake-split.md`) was compared with today's teams: every team stands at the level its table gives, apart from this branch's twelve below. Roark's split had no climb. The mini-boss aces pass `test_b1`'s boss-level check: Barry 2 at 11, Mars 1 at 20, Jupiter 1 at 29, Lucas and Dawn 2 at 31, Barry 3 at 36, Tyche and Hermes at 41 and Barry 4 at 42.

### Barry 4's stretch, against 42

Barry 4's honour cap of 42 runs from Maylene's badge to his trigger in Pastoria at (589, 828), which fires on `VAR_PASTORIA_CITY_STATE` 1 (Ian, 2026-10-31). The trigger is the one tile in front of the gym's door. With it walled off, the field model (`required.Field`) still walks from Route 213's gate across Pastoria to Route 212 South, from there to Route 212 North, and into the Pokemon Mansion. Pastoria's map lifts Route 212's blockade as it loads (`PastoriaCity_Entry0` sets `FLAG_HIDE_ROUTE_212_BLOCKADE`). So the stretch takes in Veilstone after the badge, Route 214, Valor Lakefront, Route 213 off the water, Pastoria outside the gym, both halves of Route 212, the Restaurant and the mansion.

Twelve helper-built teams from the Wake climb topped at 41 there. Each moved down one level whole, so it keeps its shape and the climb's order: Route 213's Fisherman Travis and Fisherman Kenneth; Route 212 South's Collector Dean, Policeman Danny, Scientist Stefano and Rangers Allison and Jeffrey; Route 212 North's Policemen Caleb, Dylan and Alex, Rich Boy Jason and Lady Melissa. Policeman Bobby, last in play order before the gym, keeps the stretch's one 41. No move is lost at the lower level. Travis's Wailord and Alex's Crobat now sit one under their evolution level. No test pins these levels. Tops in the stretch now:

| Top | Teams |
|---|---|
| 42 | Krystal (Ian's), Maid Clare and Lady Celeste (behind Darach), Barry 4 (his ace at his cap) |
| 41 | Policeman Bobby; Collector Jamal (Ian's); Maids Elena and Emily; Tyche and Hermes |
| 40 or under | every other ordinary team, Dahlia (40) and the Restaurant |
| 44 | Darach and Caitlin |

The gym's trainers come after Barry 4, so Wake's 44 applies to them.

## Check 3: the mandatory fights

Recounted with the split passes' method: `required.py`'s verdicts in the role table, one fixed look only (`required.moves_or_turns`), pairs fought together merged by `pairs.eye_contact`, gym trainers and bosses apart, and the story fights and gauntlet members the split docs list (their scripts and the gauntlet sections are unchanged since).

| Split | Now | At its pass | How it is made up |
|---|---:|---:|---|
| Roark | 8 | 8 (2026-10-29) | 8 by `required.py` |
| Gardenia | 12 | 12 | 7 by `required.py`, the Jubilife tag battle, Floaroma's two grunts, the Windworks grunt outside, Cheryl when first met |
| Fantina | 10 | 10 | 4 by `required.py`, the Eterna building's 6 gauntlet members |
| Maylene | 11 | 11 | 11 by `required.py` |
| Wake | 10 | 10 | 10 by `required.py`, Devon and Douglas as one double |

The trainers `required.py` reads as required but who turn, and so count as optional: Lass Sarah, Aroma Lady Taylor, Hiker Daniel and the Windworks building's grunt (Gardenia's); Hikers Justin and Jonathan (Fantina's); Breeder Jennifer and Jogger Craig (Maylene's). Somnu 1 in the Windworks is a boss.

## Check 4: the role and reward tables

`rewards.py write` regenerated `trainer-roles.tsv` and `reward-table.md` whole. In the role table, 24 trainers the split passes moved onto the story path now read required (5 in Roark's split, 7 in Gardenia's, 3 in Fantina's, 9 in Maylene's). Fishermen Andrew and Joseph sit on Route 205 South, where they moved. 59 team sizes follow the rebuilt teams. Dahlia and Darach join, and the Veilstone and Spear Pillar grunts leave, now that Tyche and Hermes are story fights. Wake's rows were already current. In the reward table only the split shares move, by a few tenths, and the count of new balls reads 0, since the Ability Capsule's ball is gone. No reward moved, and none sits on a required trainer. A second commit fixed the Jubilife grunts' split, which moved Roark's share from 4.2 to 3.8 and Gardenia's from 8.7 to 9.2.

| Check | Result |
|---|---|
| `rewards.py check` | 0 failures |
| `test_place_rewards` | passed |
| `place_rewards.py check`, on this branch's rebuilt ROM | 168 rows, each found exactly once |

## Check 5: the OxiDex's honour caps

`fights.json` now carries each mini-boss's honour cap, and beside it what the fight's script sets on the win:

| Fight | Honour cap | Win marker |
|---|---:|---|
| Barry 2 | 11 | `VAR_ROUTE_203_RIVAL_STATE` at least 1 |
| Mars 1 | 20 | `VAR_VALLEY_WINDWORKS_STATE` at least 2 |
| Jupiter 1 | 29 | `FLAG_TEAM_GALACTIC_LEFT_ETERNA_BUILDING` |
| Lucas and Dawn 2 | 31 | `VAR_ROUTE_207_COUNTERPART_TRIGGER_STATE` at least 1 |
| Barry 3 | 36 | `VAR_ROUTE_209_GATE_TO_HEARTHOME_CITY_STATE` at least 2 |
| Barry 4 | 42 | `VAR_PASTORIA_CITY_STATE` at least 2 |

The save reader takes the first of these in the save's split whose win the save does not show. Members over its cap are flagged and the fight is named ("over Jupiter 1's honour cap of 29"); once it is won, the next cap or the split's applies. Tyche and Hermes have no cap of their own, since Barry 4's covers them. `test_b1`'s `FIXED_ACES` reads the same entries, so the caps are kept in one table. The engine's cap table is unchanged.

`test_savefile` gained two checks that fail before the change and pass after: the caps in force through Fantina's and Wake's splits, and each win marker set by the script that fights it. It passes 21 of 21, every encounter tool test passes, and `test_b1` passes 48 of 48.

## Check 6: the checklist

`ingame-checklist.md` opens with a new section, "The first five splits, in play order (compiled 2026-10-31)": 28 rows, each pointing to its existing item, with the kit warp or set that reaches it and a rough time. One new item checks the OxiDex's honour caps. Mars 1, Jupiter 1, Lucas and Dawn 2, Fantina, Maylene, Barry 4 and Wake have no in-game item of their own and are met in the run.

## How it was run

On `overseer-cleanup-five`, cut from `origin/oxide` at 83b49e7697c. The ROM was built here with `make rom` after the team changes. The gate (`integrate.sh --verify-only`) ran on the branch; its result is in the branch's last commit.

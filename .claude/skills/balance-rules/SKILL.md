---
name: balance-rules
description: Ian's rulebook for Platinum Oxide's balance passes, in one place that cloud sessions can read: learnsets, later-generation moves, trainer teams, fights and how they are scored, gauntlets, items and their placement, with the pitfalls already met. Use this before proposing or writing any learnset, trainer team, item placement, TM, ability or level-cap change, before scoring or simulating a fight, and before showing Ian any balance proposal, even if the user only says "the learnset pass" or "rebalance this trainer".
---

# The balance rulebook

The balance track's status and methods live in `docs/oxide/balance-plan.md`,
and the rules every session follows live in
`.claude/rules/standing-rulings.md`. This skill gathers what a balance pass
needs from both, plus Ian's rulings that until 2026-09-27 lived only in the
Overseer's local memory. When this skill and the balance plan disagree, the
later dated ruling wins; say which in the report.

## Before any pass

- A job that rewrites game data at scale (learnsets, trainers, tables, move
  data) starts with its outcome put to Ian in one plain sentence, and a yes.
  An option word such as template, source, model or base can mean "study it"
  rather than "copy it": Kaizo's lists are a source of patterns, never copied
  line by line (2026-09-27, after a cloud job rewrote 389 species).
- Read every proposal as a player before Ian sees it: what the Pokemon has,
  when, against that split. Compare each strong move with Kaizo's placement
  for that species, and reject anything that makes a strong line stronger
  early. Ian caught Houndoom's Dark Pulse at 30 and a Flare Blitz Fletchinder
  at 33 at a glance; the proposal had not.
- Check the proposal against every ruling below, point by point, and say in
  the report that you did.

## The goal

Every Pokemon should have an important niche at the point the player has it,
while some lines stay stronger than others (Ian, 2026-09-28): Garchomp
outvalues Furret, but only one can carry Gardenia's split; Mamoswine
outvalues Aggron late, yet Aggron is one of the best physical walls. The
super-wanted lines sit marginally above average. The encounter tool's tiers
(starter-adjacent, gate, preferred, filler) are availability labels, not
intended power, so "filler" never means "may stay weak".

## Levels and splits

The caps are Roark 16, Gardenia 26, Fantina 33, Maylene 39, Wake 44, Byron
53, Candice 56, HQ 60, Galactic 65 (the Battle Zone's split), Volkner 68,
Barry 71 and League 78. Inside the Elite Four each fight's cap is its ace:
Aaron 72, Bertha 73, Flint 74, Lucian 75, Cynthia 78. The Fight Area tag
battle keeps its Beacon Badge gate, so it sits in Barry's split. Nothing is
placed past 78; a Kaizo level past its League keeps its translated place and
is listed for Ian.

## Learnsets

- **What a move is worth** is what the Pokemon knows at capture (the last four
  moves its list gives by its level, which can include moves below the catch
  level) plus what it learns afterwards. Relearner-only moves, an evolved
  form's level-1 moves among them, count for almost nothing. Level-1 lists
  still matter as the relearner's menu and as the legal palette for trainer
  teams.
- **Kaizo's placements are per species, translated by split**: find the Kaizo
  split a level falls in and carry it to the same point of the matching Oxide
  split. A Kaizo placement the player cannot reach (below the stage's
  evolution level or first catch) means the move is unavailable, not early.
  A strong move is never earlier than Kaizo's own level, but never later than
  the end of the Oxide split that level translates to.
- **Power flags**: base Speed over 100, or base Attack or Special Attack over
  100 with a move of 100 or more power of that kind the stage can have.
  Before Byron's split look closely, before Wake's very closely, and before
  Maylene's bring the line to Ian by name. A flagged stage, or one over the
  power bar (Ian's Talonflame test; its thresholds are provisional and barely
  separate anything in the first two splits), gets no strong move earlier
  than now on its own list and no new coverage ahead of its first good move
  of that type.
- **Delays** count only when waiting is a real choice. A pre-evolution kept
  back five or more levels past its evolution may reach a strong move sooner;
  that is a delay, and it stays (Houndour's Dark Pulse). Within four levels
  it counts as no wait.
- **An attack of its own type**: no stage goes more than one split without
  one of 50 effective power or more (Bonemerang counts). A stage the player
  can evolve by the end of Gardenia's split, by level or by a stone reachable
  by then, is exempt, since only a player who delays it pays. Where a
  proposal breaks the rule, the nearest such move stays at its current
  level; where that would reach a flagged stage, list it for Ian instead.
- **Status moves** are rated by `docs/oxide/status-move-tiers.md`, adjusted
  for Oxide's own values, apart from instant-death moves and the entry
  hazards other than Toxic Spikes and Sticky Web.
- **Downsides count**: lock-in (Uproar is the worst), a recharge turn, heavy
  recoil and self-drops all make a move weaker in play than its power.
- **Weak attacks** never move later and none is added. Dead weight goes:
  Absorb, Wrap, Constrict, Barrage, Snore, Rage, Razor Wind, Bide,
  Comeuppance, vanilla Octazooka and Submission are the named ones.
- No two moves on one level. Nothing that ends a wild encounter moves into
  the levels the species is met wild at. Fletchling keeps Will-O-Wisp at 25.
- **Later-generation moves**: moves vanilla Platinum's species learn by level
  up in later games come in through the same rules, as adds or as
  replacements for a weaker Generation 4 move. The source is hg-engine's
  per-game lists in `~/hg-engine` (a sparse clone, so read
  `data/learnsets/base/*.json` with `git show HEAD:<path>`). Moves later
  games give only by TM, tutor or egg wait for the TM pass. Judge a move by
  what Oxide's engine does with it (the move-pool survey's `engine_status`),
  not by whether the survey lists it. A move missing only a doubles effect
  (Flame Burst) may be placed. Lunar Blessing and Throat Chop wait for the
  element 4 follow-up; Synchronoise and the other broken ones stay out.
- Move numbers, setup PP and the no-weather rule for the player are in the
  standing rulings; they bind every learnset too.
- **Every line learns something late** (2026-09-28): each final stage the
  player can own gets at least one real level-up move at 61 or later.
- **Stone and item evolutions** (2026-09-28) get their own sparser list after
  evolving, never a copy of the pre-evolution's later moves, so evolving early
  still costs something. Evolution moves (a level-0 entry, learned on
  evolving) are used sparingly, each listed for Ian; Alolan Ninetales, reached
  from Vulpix with an Ice Stone, learns Aurora Beam that way.

## Fights and trainers

- **How a fight is judged**: a boss, which includes every named Galactic
  fight (Mars, Jupiter, Saturn, Cyrus, and officers such as Somnu or
  Hesperid), is faced with a team planned for it. An ordinary trainer or an
  unnamed grunt is faced blind, from a realistic box the run would have. The
  player uses no items during a battle (healing between fights is fine),
  never has a Life Orb or a Choice item, uses realistic movesets with their
  downsides, and plays with stalling, PP stalling, pivoting and safe setup.
- **A loss of any kind ends the run** (2026-09-28), so every fight is a
  first and only attempt; nothing may assume a retry.
- **Fight scoring is under review** (2026-09-30). The rebuilt simulator
  reached 9 of 15 held-out pairs against a bar of 13 (2026-09-27), and the
  1-to-10 scale fitted since then reads only the player's bulk. Ian's
  replacement is a perfect-line measure: how easily a line is found that wins
  with no deaths within his luck budget (every secondary status chance
  against the player happens, one crit may, never two in a row; the trainer
  uses Oxide's AI, with ties between equal picks broken at random, Ian,
  2026-09-30, replacing "the worst pick where it could choose"). The luck
  budget is retired (Ian, 2026-10-02): fights are simulated at the game's
  real odds, the planner's caution comes from how heavily it values a faint,
  and the stress test replays the chosen line with every status and crit
  check, on both sides, rolled twice and the result worse for the player
  kept (Ian, 2026-10-02). Each trainer is read on 100 simulated fights, 75 at
  real odds and 25 very unlucky (Ian, 2026-10-02). Ian's step
  2 (2026-09-30): search candidate lines (policies with responses), take the
  best, and read its clean-win rate over fresh runs, with its mean deaths
  and wipe chance beside it so the hardest fights, where no line wins
  cleanly, still separate (Wake, Barry 6). The blind prototype
  (`~/oxide-trials/scoring-review/out/`) is adopted as the direction and
  moves into this track's tools; Ian approved its six assumptions (the
  player's own luck, sleep and confusion lengths, flinches and stat drops at
  their chance, Oxide's Generation 7 crits, trainer item procs at their
  odds, freeze thawing 1 in 5 on both sides). Ian's sixteen ratings were
  made with a planned team but on an older dex and older movesets (Roark
  was always answered with Geodude), so they give direction only; his 40
  pairs are the better check, and the bar of 13 of 14 held out is too
  high (Ian, 2026-09-30). On today's data the new scorer agreed with 7
  of 15 held-out pairs and the refitted old headline with 10, so **the
  1-to-10 scale is dropped for now** (Ian, 2026-09-30): difficulty is
  judged in the scorer's own numbers (the best line's clean-win rate, mean
  deaths and wipe chance, blind or planned), Ian sets the targets for an
  average ordinary trainer, a gauntlet and a boss from example fights, and
  his first run's ratings check the scorer against real play. His targets
  (2026-09-30): an ordinary trainer, read blind, is won cleanly 70 to 80
  percent of the time with no wipe; a gauntlet section is won cleanly 60
  percent or more as a whole; too hard starts below 60 percent for an
  ordinary trainer and below 50 for a gauntlet section. The boss target
  waits until the scorer reads Roark sensibly (it reads him far too hard,
  0.30 clean with a planned team, where Ian rated him 2).
- **The scorer has its own track** (Ian, 2026-09-30): the Scoring Agent owns
  the simulator, its AI and the scorer, and trains it on the three-gym run's
  hand-played lines (`docs/oxide/trainer-scoring-handoff.md`). Ian's answers
  there bind every fight reading. A win that loses a Pokemon is a win at a
  cost, since the goal is to beat the game but each loss narrows later
  team-building, so clean wins come first. A boss is read over a spread of
  boxes, so its answers do not narrow to one Pokemon. When a fight reads too
  hard, change the player's move pools first: they are sparse in interesting
  options and lack many modern moves (his reading of Gardenia's 28 percent).
  A fight is judged on three numbers together, never the clean rate alone
  (Ian, 2026-10-01): the clean rate (won with no Pokemon fainting), the win
  rate (won at all, no wipe), and the death count (the average number of the
  player's Pokemon that faint per simulated fight), which separates the
  hardest fights, Gardenia, Wake, Cyrus 3 and Cynthia among them. The order
  ahead: the Scoring Agent's step 3, then the Kaizo study's broad comb of the
  trainers, then the full rescore (the tracker's Scheduled list). The
  scorer's good play must arise on its own from turn-by-turn search over the
  real simulator and the known trainer AI, never from named behaviours
  (Ian, 2026-10-01); a missed play is fixed in the general machinery.
- **Every trainer team is set by hand** (Ian, 2026-09-27): in the finished
  ROM no trainer keeps default moves, so default movesets carry no weight in
  any argument about learnsets or level-1 order.
- **Trainer design sits at about 6/10 of Platinum Kaizo** (2026-09-29):
  `.claude/rules/standing-rulings.md` has the whole ruling (no one-hit KO
  moves, rare evasion and trapping, at most one forced trade per boss and
  none before Fantina, no overlevelled optional trainers, some doubles).
- **Gauntlets** hold the attrition: 2 to 5 mandatory trainers on the easier
  side of their split's average, counted without optional ones; bag items may
  heal between fights; bosses stay outside, with gauntlets leading up to
  them; long areas split into sections. A majority of the game's trainers
  should be mandatory. A no-healing reading underrates a gauntlet, because one
  team has to answer several fights.
- Choice items are nearly gone from trainers too: a Choice-locked boss is
  weaker in play than its score. Trainers keep their weather.
- A trainer's nature is set through the chosen-nature field, never
  `NATURE_COUNT`, which the packer accepts and which hangs the game.

## Items

- The player never gets a Life Orb or a Choice item; type-boosting items
  (Charcoal, Mystic Water and the like) are the best offensive items.
- Evolution stones are scarce on purpose; two lines competing for one stone
  is intended. The stone census sets the counts.
- Bottle Caps work at any level and should be more common late but usable
  throughout. Exactly one Ability Patch exists. Argenta's Frontier reward is
  items, which the item pass picks. Prices are set when shops are stocked.

## TMs, tutors and egg lists

The standing rulings hold the TM rules of 2026-09-28: single-use with copies
per placement, weak TMs as rewards from one optional trainer each, about 100
TMs, Ian's removals, strong TMs no earlier than each flagged line's first good
move of that type, the HMs turned into TMs with buffs, and egg lists as the
trainers' palette only.

## Running a pass on this machine

- The replacement CPU is in and passed its checks (2026-09-29), so there is
  no job limit. A rescore still runs its agreeing second pass, which is the
  rescore's own design rather than a guard against the CPU.
- The rescore's engine hash covers `calc_headless.js`, the calculator page's
  `./calc/` scripts and the two functions lifted from `initialize.js`
  (`applyExportedMoveData`, `toImportedBaseStats`). An edit to any of them
  stales every stored score, and `test_b3` will say so.

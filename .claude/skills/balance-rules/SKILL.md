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
- **The stored score is the guide.** The rebuilt simulator reached 9 of 15
  held-out pairs against a bar of 13 and matched four of Ian's top ten
  (2026-09-27), so it is a record, not the score. Ian's own list of the
  hardest fights is the check any new scoring must keep.
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

- Until the new CPU is in: at most three heavy jobs at once across all
  sessions, each pinned to its own virtual CPU (`taskset -c`), turbo off, every result
  checked by a second run. Ask the Overseer for a slot. A Node exit of 139 is
  the CPU; rerun it.
- The rescore's engine hash covers `calc_headless.js`, the calculator page's
  `./calc/` scripts and the two functions lifted from `initialize.js`
  (`applyExportedMoveData`, `toImportedBaseStats`). An edit to any of them
  stales every stored score, and `test_b3` will say so.

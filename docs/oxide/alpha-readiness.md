# The road to QA and alpha 1

Ian's order (2026-10-06): the move rebalance and the TM pass, then his
in-game QA, then the first alpha run. Neither QA nor the alpha waits for the
Kaizo comb; the splits it has finished when the TM pass lands go in. The
Overseer updates this page as each step finishes and tells Ian, step by step.

**Status on 2026-10-06.** Step 1 is done. Steps 2 and 9 are under way. The critical path is steps 2, 3, 4, 6, 7, 8, 10, 13 and 14: roughly
two to three days, set mostly by Ian's three decision points (steps 3, 7 and
14) and the TM pass. Every estimate is a session's own or the Overseer's
guess, and says which.

| # | Step | Owner | Status | Estimate | Needs |
|---|---|---|---|---|---|
| 1 | Learnset rewrite: the 16 new checks and the new baseline | Balance Agent | done (8b05da09c1) | | |
| 2 | Learnset rewrite: the 652 lists, and its report with the checks' thresholds and the move rework proposals | Balance Agent | under way | 2 to 4 hours (its estimate) | 1 |
| 3 | Ian rules on the thresholds and the move reworks | Ian | | | 2 |
| 4 | Learnset step 5: the checks, the sealed exam, then the rewrite lands | Balance Agent, Overseer | | about 3 hours and 1.5 hours of machine time (its estimate) | 3 |
| 5 | Move reworks in the engine (rampage moves one-turn, Fury Attack and Feint out, the approved reworks), then their effects in the simulator | cloud job, then Scoring Agent | | about a day (Overseer's guess), then half a session (its estimate) | 3 |
| 6 | The reward table (every TM copy and held item, one source each, by split) and the gauntlet trainer list | Balance Agent | parts that read no learnset can start | 2 to 3 hours (its estimate) | 4 for the rest |
| 7 | Ian approves the reward table and the gauntlet list | Ian | | | 6 |
| 8 | Item data and the bigger Bag (the save break) | Balance Agent | | 2 to 3 hours, a build and a rescore (its estimate) | 7 |
| 9 | The placement tool, and the gauntlets branch brought up to `oxide` | main-track session ("pokeplatinum-fd") | under way since 2026-10-06 | 3 to 4 hours (Overseer's guess) | |
| 10 | Rewards placed in the maps, gauntlet trainers filled in, both landed | main-track session | | 3 to 6 hours (Overseer's guess) | 7, 8, 9 |
| 11 | The battle recorder logs Ian's moves (the melonDS bridge) | Overseer | not started | about half a day (Overseer's guess) | |
| 12 | The comb's finished splits go into the game, with one rescore | Overseer, Balance Agent | | a few hours | 8 |
| 13 | The QA ROM and test kit, handed to Ian | Overseer | | an hour | 4, 5, 10, 12 |
| 14 | Ian's QA pass, from `docs/oxide/ingame-checklist.md` | Ian | | a day or two | 13 |
| 15 | Goal 3's boss reading on the final box, run during QA | Scoring Agent | | 22 hours or more of machine time (its estimate) | 4, 8, 12 |
| 16 | QA's hotfixes, then the alpha 1 ROM | Overseer and the tracks | | depends on QA | 14 |

The TM pass grows the Bag, so QA starts a fresh game on step 13's ROM, and the
alpha starts another on step 16's. Doubles and tag battles stay unread in
step 15 (the tracker's backlog), and the level-cap design pass is not in
alpha 1.

## How this page is kept

The Overseer ticks a step's status the day it finishes, with its commit, and
sends Ian one line saying which step finished and which starts. A step that
slips past its estimate by half again gets a line too, with the reason. The
tracker's first-full-run entry points here and does not repeat it.

## Brief for the main-track session (steps 9 and 10)

Repo `~/pokeplatinum`. Invoke the `oxide-session` skill first, then
`carry-over-map` for the scripts and events and `save-change` before choosing
flags. Work in two worktrees: `main-placements`, cut from `oxide`, and
`main-gauntlets` (built and held at e5bf0f2cf, 318 commits behind `oxide`).

The Balance Agent's two tables, drafts until learnset step 5 closes (the
formats are settled; the rows come in step 6):

- `docs/oxide/reward-placements.tsv`, the table the placement tool reads, one
  row per placement: `reward` (item constant), `copies`, `kind` (ball,
  hidden, gift, trainer or mart), `split`, `map` (map header constant),
  `place` (the object's local id, or the mart's id), `replaces` (the item the
  place holds today, so vanilla's balls and gifts are repointed and none is
  lost), `trainer_id` (for kind trainer, the key into the next table),
  `note`.
- `docs/oxide/trainer-roles.tsv`, one row per trainer before the post-game:
  `split`, `trainer_id`, `trainer`, `map`, `object`, `required`, `role`
  (gauntlet, reward or none), `section` (the gauntlet section), `reward`,
  `copies`, `size`, `reading`, `flag`, `note`. The gauntlets read `role` and
  `section`; its reward columns are a copy for Ian, checked against the
  placements table.

Step 9, now, before the tables have rows:

1. Write `tools/oxide/place_rewards.py`, with a test. It reads
   `reward-placements.tsv` and writes each row into the map's events and
   scripts in the files' own style. A trainer reward is given once, when the
   player talks to the trainer after beating them, under a spare flag. A
   checker reads every placement back out of the built ROM with
   `scriptdis.py` and finds each table row exactly once. Use the TM pass
   draft's table (`docs/oxide/tm-pass.md` on `origin/balance-learngen-v2`,
   read with `git show`) as test data only. Commit no placements from it.
2. Merge `oxide` into `main-gauntlets`, rebuild, and run the gate.

Step 10, when Ian has approved the reward table and the gauntlet list:

3. Apply the table. Vanilla's TM balls and gifts are repointed, the new
   trainer rewards and balls added, and every changed map named in the
   `DIVERGED` lists of `bulk_scripts.py` and `bulk_events.py` with the reason,
   so the restart checks never regenerate it from the base ROM.
4. Fill in the gauntlets' trainer table from the approved list.
5. Build, run `bash tools/oxide/integrate.sh --verify-only`, add test-kit warps
   for a sample (one ball, one trainer reward, one gift, one gauntlet), and
   write their checks into `docs/oxide/ingame-checklist.md`. The Overseer
   lands each branch with `merge-branch.sh`.

Rules that bite: stage files by name; never reformat a `res/` JSON file;
never launch an emulator; edit only `res/field/`, `res/text/` where a reward
needs a line, `tools/oxide/place_rewards.py` and its test, the two `DIVERGED`
lists, the test kit and the checklist, and ask the Overseer before anything
else. A spare flag moves nothing in the save, but check it with the
`save-change` skill.

Done means the checker finds every row exactly once, the gate passes, and the
test kit reaches the sample. Report to the Oxide Overseer with SendMessage at
the end of each step: a one-page summary first (what changed, what was
checked and how, what waits on Ian, how long the next step takes), failures
first.

Ian's writing rules bind every report, comment and commit message. The hard
rules, quoted from `~/.claude/CLAUDE.md`:

```
- No em-dashes or en-dashes as punctuation. Use a comma, a full stop, a colon,
  or parentheses. This applies inside code comments and commit messages too.
- No opening praise or acknowledgement ("Great question", "Good catch",
  "You're right to ask"). Start with the answer.
- No closing offers or sign-offs ("Let me know if", "Hope this helps",
  "Happy to", "Feel free to"). Stop when the content stops.
- Prose over bullets. A list is for genuinely parallel items (files, steps,
  options, findings). Argument, explanation and narrative are paragraphs.
- No bold-label bullets that are really paragraphs in disguise, and no headers
  in anything under about five hundred words.
- Do not assume Ian is the expert on a question he asked. Answer it.
- Annotate code in plain English: what it does and why, not what the syntax is.
```

# The road to QA and alpha 1

Ian's order (2026-10-06): the move rebalance and the TM pass, then his
in-game QA, then the first alpha run. Neither QA nor the alpha waits for the
Kaizo comb; the splits it has finished when the TM pass lands go in. The
Overseer updates this page as each step finishes and tells Ian, step by step.

**Status on 2026-10-07.** Steps 1 to 11 and 17 are done, the combined branch landed at 787c581c8 (gate 50 of 50), and QA runs on QA ROM 1 (step 13). Next: the AI flags pass and the simulator's updates land (step 18), step 12 puts the comb's drafts in with a small rescore, and step 15 reads that commit during QA.
two to three days, set mostly by Ian's three decision points (steps 3, 7 and
14) and the TM pass. Every estimate is a session's own or the Overseer's
guess, and says which.

| # | Step | Owner | Status | Estimate | Needs |
|---|---|---|---|---|---|
| 1 | Learnset rewrite: the 16 new checks and the new baseline | Balance Agent | done (8b05da09c1) | | |
| 2 | Learnset rewrite: the 652 lists, and its report with the checks' thresholds and the move rework proposals | Balance Agent | done: landed at 085f72211 after a second loop (Ian, 2026-10-06), gate 48 of 48 | 2 to 4 hours (its estimate) | 1 |
| 3 | Ian rules on the thresholds and the move reworks | Ian | done: the reworks accepted as listed, the late shortfall and named cases left for after the alpha (2026-10-06) | | 2 |
| 4 | Learnset step 5: the checks, the sealed exam, then the rewrite lands (boss bands wait for step 15) | Balance Agent, Overseer | exam judged: fails in part (`learnset-exam.md`, its last section); done: the rewrite landed at 085f72211; Leafeon's and Sylveon's late start (a rock or Charm, not a level) is fixed in the TM pass | about 3 hours and 1.5 hours of machine time (its estimate) | 3 |
| 5 | Move reworks in the engine (rampage moves one-turn, Fury Attack and Feint out, the approved reworks, and Upper Hand, Shell Trap and Burning Jealousy made to work), then their effects in the simulator | cloud job, then Scoring Agent | done: the engine's reworks and the simulator's update landed with the combined branch at 787c581c8 (2026-10-07), gate 50 of 50 | about a day (Overseer's guess), then half a session (its estimate) | 3 |
| 6 | The reward table (every TM copy and held item, one source each, by split) and the gauntlet trainer list, with the Leafeon and Sylveon fix | Balance Agent | done: the table frozen at Ian's approval, four TMs repriced; landed with the combined branch at 787c581c8 (2026-10-07), gate 50 of 50 | the table's draft within the hour, then the ladders, then one rescore after the cloud job merges (its estimate) | 4 |
| 7 | Ian approves the reward table and the gauntlet list | Ian | done (2026-10-06 and 2026-10-07) | | 6 |
| 8 | Item data and the bigger Bag (the save break) | the main-track session (the Bag and the TM item records, from 2026-10-06), the Balance Agent (each species' TM compatibility and the rescore) | done: the Bag, the TM items, single-use HMs and every species' TM compatibility, with a read-back check in the gate; landed with the combined branch at 787c581c8 (2026-10-07), gate 50 of 50 | 2 to 3 hours, a build and a rescore (its estimate) | 7 |
| 9 | The placement tool, and the gauntlets branch brought up to `oxide` | main-track session ("pokeplatinum-fd") | done: the tool landed (c82ffe884) and its test is in the gate; `main-gauntlets` is up to date (a82e550cb) and held for step 10 | 3 to 4 hours (Overseer's guess) | |
| 10 | Rewards placed in the maps, gauntlet trainers filled in, the shop and Game Corner TMs gated by badges and sold once each, all landed; Solaceon's three vendors in the north house removed (Ian, 2026-10-07) | main-track session | done: the table applied (165 rows), the gift lines, the gauntlets, the shop gating, Solaceon's and the Survival Area's vendors removed; landed with the combined branch at 787c581c8 (2026-10-07), gate 50 of 50 | 7, 8, 9 |
| 11 | The battle recorder logs Ian's moves (the melonDS bridge) | Overseer | built: game side landed (0a27a2b0d), the fork's `beacon-moves` (633a39c) and the recorder ready; Ian swaps in the new melonDS build, and the live check is in QA (checklist, section 1) | about half a day (Overseer's guess) | |
| 12 | Every team the comb has finished goes into the game, later bosses included, with one rescore; first the Kaizo study sweeps its teams for moves the final lists no longer allow; Wake keeps today's team for the alpha (Ian, 2026-10-07); every finished draft goes in as drafted, with no retuning (Ian, 2026-10-07), Wake keeping today's team; Ian chooses any retunes from step 15's readings | Overseer, Balance Agent | | a few hours | 8 |
| 13 | The QA ROM and test kit for Ian's bug checks, cut from the combined branch (`qa-rom-1`: `balance-tm-pass` with `main-tm-items`) without waiting for the rescore or the comb (Ian, 2026-10-07: QA needs the game, not the scores); a later ROM with step 12's teams keeps the same save, since step 12 changes only trainer data | Overseer | under way 2026-10-07: built and gated on `qa-rom-1` | 5, 10 |
| 14 | Ian's QA pass, from `docs/oxide/ingame-checklist.md` | Ian | | a day or two | 13 |
| 15 | Goal 3's boss reading on the final box, run during QA, of the trainer files on the commit that lands step 12 (the teams the alpha will hold), not the QA ROM's | Scoring Agent | | about 35 hours of machine time (its estimate): 22 to 23 for the 39 bosses by team search, 9 to 17 for the 41 Ace Trainers read blind; the 8 tag battles wait for doubles | 4, 8, 12 |
| 17 | The alpha checklist in the OxiDex: every zone in walking order with its trainers, rewards, items and checks, a feedback spot for each trainer, ticks read from the save | encounter track | done: stage A (the Alpha tab) landed at 6d75b0350c and stage B (feedback spots, ticks from the save, export) at 7389bd326f, both on 2026-10-07; Ian's layout notes (sprite and text size, the rivals' versions folded) are being worked | 14 to 16 hours in two stages (its estimate); took about 8 | data final after 10 and 12; builds now |
| 18 | The AI flags pass: the nine flags beyond Expert and Basic (Setup First Turn, Check HP, Harassment, Baton Pass, Risky, Prioritize Extremes, Weather, Tag Strategy, Evaluate Attack) route each new move as its nearest Platinum effect, as Expert's pass did, and the scorer mirrors it; the bosses carrying a changed flag are re-read in step 16 | cloud job, then Scoring Agent | done: the AI flags pass (21 moves in six flags, Ian accepted the calls as built) and Expert for five more moves landed at 4bd54eb36, the simulator's mirror with the end-of-turn order fix at df365a296 (2026-10-07) | about half a day (Overseer's guess) | 13 |
| 16 | QA's hotfixes, then the alpha 1 ROM; any boss team landed after step 13 is read before the ROM is fixed | Overseer and the tracks, Scoring Agent | | depends on QA; 1 to 2 hours of machine time for one re-read boss, about 35 minutes each when several are read together (the Scoring Agent's estimate) | 14, 15, 18 |

The scorer reads only the teams in the ROM Ian plays, never the study's working files, so its boss order and Ian's ratings describe the same fights (a side agent's catch, 2026-10-06). It does so on an extraction of the ROM's commit (`git archive`), with the boxes rebuilt on it; the Scoring Agent proved the route on a planted edit the same day, with no code change. The TM pass grows the Bag, so QA starts a fresh game on step 13's ROM, and the
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
   scripts in the files' own style. A trainer reward is given automatically
   straight after the player wins, once, under its own spare flag (Ian,
   2026-10-06, relayed by the main track); talking to the trainer again
   retries only if the Bag was full the first time. A
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
needs a line, `include/data/field/hidden_items.h` and `include/data/mart_items.h`
for hidden-item and mart rows, `tools/oxide/place_rewards.py` and its test,
the two `DIVERGED` lists, the test kit and the checklist, and ask the Overseer before anything
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

## Brief for the encounter track (step 17, the alpha checklist)

Ian, 2026-10-06: "a zone-by-zone checklist of things I should verify when we
get to the alpha test within Oxidex. For example, when I get to Route 202, I
should fight x mandatory trainers, y optional trainers with z rewards, x
hidden items, etc. Especially if each trainer at that location has a spot for
feedback." It also carries the run plan's notes log (the tracker's
first-full-run entry, items 6 and 7).

Done means each of these checks passes, each verified by the session unless
marked:

1. An "Alpha checklist" page in the OxiDex lists every zone in walking order,
   grouped by split, generated from the game's data at load time, so it
   follows every later change (the reward placements of step 10, the combed
   teams of step 12) without hand edits.
2. Each zone lists its mandatory trainers, optional trainers with their
   rewards, gauntlet sections, item balls with their contents, hidden items,
   gifts, shop and Game Corner TMs with their badge counts, and its wild
   encounters. A test checks each count against the data.
3. Each trainer row shows its team (species and levels from
   `res/trainers/data/`) and has a feedback spot: fought, a rating out of 10
   for bosses and gauntlet sections, a free note, and a death note (which
   fight, what killed it, whether Ian saw it coming). Each note is stamped
   with the ROM's commit, the location, the badges and the party, from the save
   and the live bridge where they answer.
4. Rows tick themselves where the save can tell: trainers beaten and items
   picked up, from the save's flags. A test save ticks the right rows.
5. Each zone shows the in-game checks from `docs/oxide/ingame-checklist.md`
   that belong to it; every checklist item maps to a zone or to "anywhere".
6. Feedback saves to a local per-playthrough file (gitignored, as
   `caught.json` is) and survives a restart. An export writes it to a notes
   file in the repo for the other sessions, and reads back.
7. Ian checks the page in his browser on today's data (Ian).

Sources: `docs/oxide/trainer-roles.tsv` and `docs/oxide/reward-placements.tsv`
(on `balance-tm-pass` until it lands; read them from `oxide` after),
`docs/oxide/tm-list.tsv`, the events files and `include/data/field/hidden_items.h`
for balls and hidden items, the tool's own scripted sources for gifts, and
the encounter tables. Work on the track's own branch; the Overseer lands it
and restarts Ian's server. Send the Overseer an estimate before starting, and
a one-page summary at the end.


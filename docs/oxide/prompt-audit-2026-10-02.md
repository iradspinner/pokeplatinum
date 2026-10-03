# Prompt audit of the Claude Code configuration, 2026-10-02

Run with `/doctor prompt-audit` on 2026-10-02, by the Oxide Overseer, against the
bundled `claude-api` skill's prompt-audit guide. This is a report and a proposed
diff only: no instruction file was changed.

## Assumptions

**Scope**, as the request set it: the Claude Code configuration that loads into
sessions in this project.

- In the project: `CLAUDE.md`, `.claude/rules/` (2 files),
  `.claude/skills/*/SKILL.md` (14 skills, none with reference files) and
  `.claude/commands/` (3 commands). There is no `.claude/CLAUDE.md`,
  `AGENTS.md`, `CLAUDE.local.md`, nested `CLAUDE.md`, subagent definition or
  output style, and no `CLAUDE.md` imports another file.
- At user level, affecting every project: `~/.claude/CLAUDE.md`, and the 16
  skills synced into `~/.claude/skills/synced/` from Ian's claude.ai account.
  There are no user-level rules, commands, subagents or output styles.
- Installed plugins, report only: the skills, commands and subagents of the
  synced plugins (bio-research, cowork-plugin-management, data, design,
  desktop-commander, engineering, marketing, modern-web-guidance, pdf-viewer,
  product-management, productivity, sales). The marketplace clone under
  `~/.claude/plugins/marketplaces/` holds plugins that are not installed, and
  `.trash/` holds removed ones; neither was audited.
- No managed-policy `CLAUDE.md` exists (`/etc/claude-code/` is absent), and no
  ancestor directory holds an instruction file.

**Skipped:** settings files, `.mcp.json` and `~/.claude.json` (not prompt
text, and they can hold secrets); the 26 git worktrees under
`.claude/worktrees/`, which are other branches' checkouts carrying their own
copies of these files; and the memory folder, which the request did not name.

**Target model:** Claude Opus 5.5, the model running this audit. No skill,
command or subagent pins a model of its own.

## Summary

The project's own instruction files carry almost no dated prompting: no
capitalised emphasis, no thinking scaffolds, no numeric output caps, no
retired model names and no tool discouragement. The guide's greppable signals
found nothing in them. What the audit found is facts the project has
outgrown, nearly all from the last four days: the new CPU of 2026-09-29, the
private GitHub builder retired on 2026-10-01, and Ian's fight-scoring rulings
of 2026-09-30 to 2026-10-02.

The three that matter most:

1. **The balance rulebook contradicts itself on how a fight is scored.** Its
   fight-scoring section has accreted three days of rulings and still says
   "so clean wins come first", ten lines above Ian's ruling of 2026-10-02 that
   lines are ranked by win rate first and the clean rate is reported, not
   optimised. It also says the scorer reads Roark "far too hard, 0.30 clean",
   where the planner now reads him at 97.7% and goal 1 is passed. A balance
   session reads this skill before any fight work.
2. **The cloud-job skill still sends landings to GitHub.** It says
   `merge-branch.sh` "builds the merged tree on GitHub", says cloud VMs take
   "the work this box's CPU cannot", and says to "fetch" a test-kit ROM. Each
   is false since 2026-09-29 or 2026-10-01.
3. **Two skills disagree on how the doc server is restarted.** `doc-links` says
   the encounter tool builder's session restarts it from its own worktree;
   `land-branch`, written later the same day, says it runs from
   `.claude/worktrees/ian-tool` and is restarted with `restart_server.sh`.

Counts: Group 1 (dated prompt text), 3 findings, all migration-relative
phrasing in the project's files, plus report-only signals in the plugins and
synced skills. Group 2 (brittle configuration files), 18 findings: 9 high, 4
medium, 5 low or flag. Group 3 (tool descriptions): not applicable, since no
tool definitions are in scope. Group 4 (request code and architecture): not
applicable, since there is no request-building code and no subagent roster.

## Findings in the project's files

Ordered by confidence. "The diff" below has a hunk for each high and medium
finding.

| # | Location | Evidence | Pattern | Why it no longer fits | Confidence | Action |
|---|---|---|---|---|---|---|
| H1 | `.claude/skills/cloud-job/SKILL.md:94-97` | `It merges, builds the merged tree on GitHub, runs the full gate on that ROM` | Group 2, volatile specifics | `merge-branch.sh` builds here since 2026-09-29 (its own header, and CLAUDE.md's Tools paragraph) | High | rewrite: "builds the merged tree here" |
| H2 | `.claude/skills/cloud-job/SKILL.md:8-9` | `so they take the work this box's CPU cannot` | Group 2, volatile specifics | CLAUDE.md: the replacement CPU passed its checks, with no job limit | High | rewrite: cloud VMs take long jobs without tying this machine up |
| H3 | `.claude/skills/cloud-job/SKILL.md:109-110` | `Fetch a test-kit ROM if the job added kit entries` | Group 2, volatile specifics | `fetch-rom` was deleted on 2026-10-01; the test kit is built with `make testkit` | High | rewrite |
| H4 | `.claude/skills/read-donor/SKILL.md:71-73` | `done on cloud/element7-items and not yet merged` | Group 2, volatile specifics | the tracker's Phase 4 item 7 is ticked: element 7 merged on 2026-09-27 and 28 | High | rewrite: merged |
| H5 | `.claude/skills/balance-rules/SKILL.md:100-101` | `Lunar Blessing and Throat Chop wait for the element 4 follow-up` | Group 2, volatile specifics | the tracker: both are done on `main-production` (2026-09-30), and the later-moves report can now place them | High | remove that clause |
| H6 | `.claude/skills/balance-rules/SKILL.md:123-188` | `so clean wins come first` (167) beside `Lines are ranked by win rate first and average faints second` (176); `it reads him far too hard, 0.30 clean` (160); `The order ahead: the Scoring Agent's step 3, then the Kaizo study's broad comb` (183) | Group 2, contradiction within one file and history narratives; Group 1d, patch accretion | Ian's ruling of 2026-10-02 replaced "clean wins come first"; goal 1 passed at 97.7% clean; his four goals put the comb after goal 2 | High | rewrite both bullets as one statement of the current rules (in the diff) |
| H7 | `.claude/skills/oxide-session/SKILL.md:27-33, 101-102` | the list of tracks and status homes ends at `The balance track` | Group 2, contradiction | CLAUDE.md names five tracks; the scoring track's status home is `docs/oxide/trainer-scoring-handoff.md` | High | add the scoring track |
| H8 | `.claude/skills/doc-links/SKILL.md:64-66` | `The server on 8765 runs from the encounter tool builder's worktree ... until that session restarts it; ask it to.` | Group 2, files contradict each other | `land-branch/SKILL.md:56-62` (9894bf8c3c, 2026-09-27 19:56) is newer than this passage (f27432c53f, 02:59 the same day), and `.claude/worktrees/ian-tool` and `restart_server.sh` both exist | High | rewrite to match land-branch |
| H9 | `.claude/skills/playtest-day/SKILL.md:3` (description) | `from fetching the right ROMs` and `the new CPU has arrived` | Group 2, volatile specifics, in trigger text | the CPU arrived on 2026-09-29, and the skill's own body builds the ROMs locally | High | rewrite; the description's trigger list otherwise stays |
| M1 | `CLAUDE.md:106-112` | `The replacement CPU is in and passed its checks (2026-09-29). The old i9-14900K was degraded ...` | Group 2, history narrative | the file every session loads tells the CPU's story; the lesson is already in the design doc's findings log (2026-09-22), and the rule that matters now, the memory cap, is missing | Medium | rewrite to the current rule |
| M2 | `.claude/rules/standing-rulings.md:95-98` | `so the three-job limit of 2026-09-27 is lifted` | Group 2, history narrative | the limit no longer exists; only the rule that local builds are trusted is live | Medium | rewrite |
| M3 | `.claude/skills/carry-over-map/SKILL.md:60` | `before GitHub builds the ROM` | Group 2, volatile specifics | builds are local | Medium | rewrite |
| M4 | `.claude/skills/balance-rules/SKILL.md:227-229` | `The replacement CPU is in and passed its checks (2026-09-29), so there is no job limit.` | Group 2, history narrative | the CPU is history; the live rule is the memory cap of 2026-10-02 | Medium | rewrite |
| M5 | `.claude/skills/oxide-session/SKILL.md:140-142` | `Ian's default model is Opus now, so a subagent no longer saves anything` | Group 1d, migration-relative phrasing with a pinned model | "now" and "no longer" describe a change the reader never saw | Medium | rewrite without the model name |
| M6 | `.claude/rules/standing-rulings.md:110-112` | `replacing the budget of 2026-09-30, under which every secondary status against the player landed and one crit could` | Group 1d, migration-relative phrasing | the rule reads as a diff against a retired one | Medium | remove the history clause |
| M7 | `.claude/skills/read-donor/SKILL.md:53-54` | `since element 4, so the move id is no longer capped at 511` | Group 1d, migration-relative phrasing | the same | Medium | rewrite |
| L1 | `.claude/skills/cloud-job/SKILL.md:33-34` | `Opus 5.5 at Medium for a data pass ... at High for anything touching the type chart` | Group 2, pinned model names | a pinned model degrades after the next release, and Ian's stated preference elsewhere is effort up front | Low | flag: state the criteria, or keep as a dated choice |
| L2 | `.claude/skills/land-branch/SKILL.md:9-10` | `(under a minute)` and `(about two minutes)` | Group 2, volatile specifics | the landings of 2026-10-01 and 02 took several minutes end to end, with the planner's jobs running beside them | Low | flag |
| L3 | `.claude/skills/balance-rules/SKILL.md:11-12` | `Ian's rulings that until 2026-09-27 lived only in the Overseer's local memory` | Group 2, history narrative | archaeology, harmless | Low | flag |
| L4 | `.claude/rules/standing-rulings.md` | `Ian's user settings (~/.claude/settings.json) are his to edit. Hand him the exact change instead.` | Group 2, a possible conflict with a file out of scope | on 2026-10-02 Ian chose a different route, recorded only in local memory: the session builds the file, he approves the refused install in `/permissions`, the session installs it. Whether the standing rule changes is his call | Low | flag |
| L5 | `CLAUDE.md:157-158` | `The environment passed its smoke test on 2026-09-25` | Group 2, history narrative | a dated result in the always-loaded file | Low | flag |

**Checked and clean:** every repo path the files name resolves (the few that
do not are outside the repo by design: the `xlsx` skill's `recalc.py`, the G:
drive's generator scripts, hg-engine's `CONFIG.md`, memory's `MEMORY.md`).
The `port-element` skill's claims about taken state bits match
`include/constants/battle/`. The repo copy of the writing rules
(`.claude/rules/writing.md`) agrees with `~/.claude/CLAUDE.md` word for word,
apart from its header comment, so that duplication is working, not cruft.
`~/.claude/CLAUDE.md` itself has no findings: its banned-phrase list is
Ian's stated preference, with its reason in its heading and a hook enforcing
it, and its formatting rules are conditional ones, which the guide keeps.

## Plugins and synced user skills (report only)

These are managed by Ian's claude.ai account and the plugin marketplace, so an
edit here would be overwritten on the next sync; no change is proposed.

| Source | Signal | Count | First example |
|---|---|---|---|
| plugin bio-research | capitalised emphasis (Group 1a) | 12 | `instrument-data-to-allotrope/SKILL.md:61`: `**IMPORTANT:** Separate raw measurements from calculated` |
| plugin modern-web-guidance | capitalised emphasis | 5 | `chrome-extensions/SKILL.md:30`: `you MUST create the actual image files` |
| plugin sales | numeric output caps (Group 1f) | 6 | `inbox-sweep/SKILL.md:86`: `under 120 words` |
| plugin product-management | numeric output caps; hedged requirements | 6; 2 | `stakeholder-update/SKILL.md:69`: `Keep it under 300 words.` |
| plugin marketing | numeric output caps | 2 | `content-creation/SKILL.md:35`: a headline `in under 10 words` (a format-sensitive length, arguably kept) |
| plugin data, desktop-commander | capitalised emphasis or hedges | 1 to 3 each | |
| user skill canvas-design | capitalised emphasis | 10 | `canvas-design/SKILL.md:22`: `THE CRITICAL UNDERSTANDING` |
| user skills skill-creator, pptx, pdf | capitalised emphasis or hedges | 1 to 6 each | |

None of the plugin or synced files names a retired model or carries a
thinking scaffold.

## The proposed diff

One hunk per finding, H1 to H9 and M1 to M7. Paths are relative to the repo
root. Apply hunks selectively; each rewrite keeps the live purpose of the line
it replaces. The H6 hunk replaces the balance rulebook's two fight-scoring
bullets with one statement of the current rules and points at the standing
rulings and the tracker rather than repeating their dates.

```diff
diff -ru a/.claude/rules/standing-rulings.md b/.claude/rules/standing-rulings.md
--- a/.claude/rules/standing-rulings.md
+++ b/.claude/rules/standing-rulings.md
@@ -92,10 +92,8 @@
   almost nothing: the relearner is in Pastoria, each move costs a scarce Heart
   Scale, and each use competes with every other in the box. Level-1 lists
   matter as the relearner's menu and the legal palette for trainer teams.
-- The replacement CPU is in and passed its stress and build checks
-  (2026-09-29), so the three-job limit of 2026-09-27 is lifted and local
-  builds are trusted: a ROM counts when its SHA-1 matches GitHub's build of
-  the same commit.
+- Local builds are trusted (2026-09-29): a ROM counts when its SHA-1
+  matches GitHub's build of the same commit.
 - How the fight scorer reads a fight (Ian, 2026-09-30, on the trainer-scoring
   handoff). The aim is to beat the game: a win that loses a Pokemon is still a
   win, but each loss takes away later team-building options. Lines are ranked
@@ -107,9 +105,8 @@
   reported, not optimised. A boss is read
   over a spread of rolled boxes, so that its answers do not narrow to one
   Pokemon. Ties between equal AI picks break at random. Every fight is
-  simulated at the game's real odds, with no luck budget (Ian, 2026-10-02,
-  replacing the budget of 2026-09-30, under which every secondary status
-  against the player landed and one crit could): the three numbers are then
+  simulated at the game's real odds, with no luck budget (Ian, 2026-10-02):
+  the three numbers are then
   true frequencies with bad luck inside them, and the planner's caution
   comes from how heavily a position values a faint, weighing each chance at
   its true odds. The stress test that replaces the budget (Ian, 2026-10-02)
diff -ru a/.claude/skills/balance-rules/SKILL.md b/.claude/skills/balance-rules/SKILL.md
--- a/.claude/skills/balance-rules/SKILL.md
+++ b/.claude/skills/balance-rules/SKILL.md
@@ -97,8 +97,8 @@
   games give only by TM, tutor or egg wait for the TM pass. Judge a move by
   what Oxide's engine does with it (the move-pool survey's `engine_status`),
   not by whether the survey lists it. A move missing only a doubles effect
-  (Flame Burst) may be placed. Lunar Blessing and Throat Chop wait for the
-  element 4 follow-up; Synchronoise and the other broken ones stay out.
+  (Flame Burst) may be placed. Synchronoise and the other broken ones stay
+  out.
 - Move numbers, setup PP and the no-weather rule for the player are in the
   standing rulings; they bind every learnset too.
 - **Every line learns something late** (2026-09-28): each final stage the
@@ -120,72 +120,30 @@
   downsides, and plays with stalling, PP stalling, pivoting and safe setup.
 - **A loss of any kind ends the run** (2026-09-28), so every fight is a
   first and only attempt; nothing may assume a retry.
-- **Fight scoring is under review** (2026-09-30). The rebuilt simulator
-  reached 9 of 15 held-out pairs against a bar of 13 (2026-09-27), and the
-  1-to-10 scale fitted since then reads only the player's bulk. Ian's
-  replacement is a perfect-line measure: how easily a line is found that wins
-  with no deaths within his luck budget (every secondary status chance
-  against the player happens, one crit may, never two in a row; the trainer
-  uses Oxide's AI, with ties between equal picks broken at random, Ian,
-  2026-09-30, replacing "the worst pick where it could choose"). The luck
-  budget is retired (Ian, 2026-10-02): fights are simulated at the game's
-  real odds, the planner's caution comes from how heavily it values a faint,
-  and the stress test replays the chosen line with every status and crit
-  check, on both sides, rolled twice and the result worse for the player
-  kept (Ian, 2026-10-02). Each trainer is read on 100 simulated fights, 75 at
-  real odds and 25 very unlucky (Ian, 2026-10-02). Ian's step
-  2 (2026-09-30): search candidate lines (policies with responses), take the
-  best, and read its clean-win rate over fresh runs, with its mean deaths
-  and wipe chance beside it so the hardest fights, where no line wins
-  cleanly, still separate (Wake, Barry 6). The blind prototype
-  (`~/oxide-trials/scoring-review/out/`) is adopted as the direction and
-  moves into this track's tools; Ian approved its six assumptions (the
-  player's own luck, sleep and confusion lengths, flinches and stat drops at
-  their chance, Oxide's Generation 7 crits, trainer item procs at their
-  odds, freeze thawing 1 in 5 on both sides). Ian's sixteen ratings were
-  made with a planned team but on an older dex and older movesets (Roark
-  was always answered with Geodude), so they give direction only; his 40
-  pairs are the better check, and the bar of 13 of 14 held out is too
-  high (Ian, 2026-09-30). On today's data the new scorer agreed with 7
-  of 15 held-out pairs and the refitted old headline with 10, so **the
-  1-to-10 scale is dropped for now** (Ian, 2026-09-30): difficulty is
-  judged in the scorer's own numbers (the best line's clean-win rate, mean
-  deaths and wipe chance, blind or planned), Ian sets the targets for an
-  average ordinary trainer, a gauntlet and a boss from example fights, and
-  his first run's ratings check the scorer against real play. His targets
-  (2026-09-30): an ordinary trainer, read blind, is won cleanly 70 to 80
-  percent of the time with no wipe; a gauntlet section is won cleanly 60
-  percent or more as a whole; too hard starts below 60 percent for an
-  ordinary trainer and below 50 for a gauntlet section. The boss target
-  waits until the scorer reads Roark sensibly (it reads him far too hard,
-  0.30 clean with a planned team, where Ian rated him 2).
-- **The scorer has its own track** (Ian, 2026-09-30): the Scoring Agent owns
-  the simulator, its AI and the scorer, and trains it on the three-gym run's
-  hand-played lines (`docs/oxide/trainer-scoring-handoff.md`). Ian's answers
-  there bind every fight reading. A win that loses a Pokemon is a win at a
-  cost, since the goal is to beat the game but each loss narrows later
-  team-building, so clean wins come first. A boss is read over a spread of
-  boxes, so its answers do not narrow to one Pokemon. When a fight reads too
-  hard, change the player's move pools first: they are sparse in interesting
-  options and lack many modern moves (his reading of Gardenia's 28 percent).
-  The scorer reads the first three splits under interim soft caps at their
-  mini-bosses (Ian, 2026-10-02): Barry 2's ace (11) until he is beaten, Mars
-  1's Purugly (19), Jupiter 1's Skuntank (27), and each Lucas and Dawn fight
-  in those splits at its own ace's level; a stand-in for more caps Ian
-  may add to the game.
-  Lines are ranked by win rate first and average faints second (Ian,
-  2026-10-02): always winning with one sacrifice beats winning cleanly nine
-  times in ten; the clean rate is reported, not optimised.
-  A fight is judged on three numbers together, never the clean rate alone
-  (Ian, 2026-10-01): the clean rate (won with no Pokemon fainting), the win
-  rate (won at all, no wipe), and the death count (the average number of the
-  player's Pokemon that faint per simulated fight), which separates the
-  hardest fights, Gardenia, Wake, Cyrus 3 and Cynthia among them. The order
-  ahead: the Scoring Agent's step 3, then the Kaizo study's broad comb of the
-  trainers, then the full rescore (the tracker's Scheduled list). The
-  scorer's good play must arise on its own from turn-by-turn search over the
-  real simulator and the known trainer AI, never from named behaviours
-  (Ian, 2026-10-01); a missed play is fixed in the general machinery.
+- **How a fight is scored** (Ian's rulings of 2026-09-30 to 2026-10-02; the
+  standing rulings hold them whole). The Scoring Agent owns the simulator,
+  its AI and the scorer (`docs/oxide/trainer-scoring-handoff.md`). The scorer
+  is a turn-by-turn planner whose good play arises from search over the real
+  simulator and the exactly known trainer AI, never from named behaviours; a
+  missed play is fixed in that general machinery. Fights run at the game's
+  real odds, with ties between equal AI picks at random. Each trainer is read
+  on 100 simulated fights, 75 at real odds and 25 very unlucky (every status
+  and crit check on both sides rolled twice, the result worse for the player
+  kept). A fight is judged on three numbers together: the clean rate, the win
+  rate and the average faints. Lines and the planner's options are ranked by
+  win rate first and average faints second; the clean rate is reported, not
+  optimised, since always winning with one sacrifice beats winning cleanly
+  nine times in ten. Exact ties break toward the faster finish. Bosses are
+  read over a spread of boxes, so their answers do not narrow to one Pokemon.
+  The first three splits are read under interim soft caps at their
+  mini-bosses (Barry 2's ace 11, Mars 1's Purugly 19, Jupiter 1's Skuntank 27,
+  Lucas and Dawn 2 at 30). Ian's first targets (an ordinary trainer, read
+  blind, 70 to 80 percent clean with no wipe; a gauntlet section 60 percent or
+  more) were set before these rulings and are provisional until his first
+  run. When a fight reads too hard, change the player's move pools first: they
+  are sparse in interesting options and lack many modern moves. The scorer's
+  goals, the Kaizo study's comb and the full rescore come in the order the
+  tracker's Scoring Agent entry and Scheduled list give.
 - **Every trainer team is set by hand** (Ian, 2026-09-27): in the finished
   ROM no trainer keeps default moves, so default movesets carry no weight in
   any argument about learnsets or level-1 order.
@@ -224,9 +182,8 @@
 
 ## Running a pass on this machine
 
-- The replacement CPU is in and passed its checks (2026-09-29), so there is
-  no job limit. A rescore still runs its agreeing second pass, which is the
-  rescore's own design rather than a guard against the CPU.
+- There is no job limit; heavy or parallel jobs run under
+  `tools/oxide/capped`. A rescore runs its agreeing second pass by design.
 - The rescore's engine hash covers `calc_headless.js`, the calculator page's
   `./calc/` scripts and the two functions lifted from `initialize.js`
   (`applyExportedMoveData`, `toImportedBaseStats`). An edit to any of them
diff -ru a/.claude/skills/carry-over-map/SKILL.md b/.claude/skills/carry-over-map/SKILL.md
--- a/.claude/skills/carry-over-map/SKILL.md
+++ b/.claude/skills/carry-over-map/SKILL.md
@@ -57,7 +57,7 @@
 tool paths `ninja -t commands` prints for that script. Disassembling the output
 with `scriptdis.emit_source` and diffing it against the base ROM's member shows
 every change command by command, and catches a movement block pushed off
-alignment before GitHub builds the ROM.
+alignment before the ROM is built.
 
 For a script you cannot read, `python3 tools/oxide/scriptdis.py` disassembles
 any member of either ROM; `--roundtrip` proves the emitter, and
diff -ru a/.claude/skills/cloud-job/SKILL.md b/.claude/skills/cloud-job/SKILL.md
--- a/.claude/skills/cloud-job/SKILL.md
+++ b/.claude/skills/cloud-job/SKILL.md
@@ -5,8 +5,8 @@
 
 # A cloud job, end to end
 
-Cloud sessions run on healthy four-core VMs, so they take the work this box's
-CPU cannot: engine changes that need many builds. They cannot see the base
+Cloud sessions run on four-core VMs apart from this machine, so they take long
+jobs (engine changes that need many builds) without tying it up. They cannot see the base
 ROM, the vanilla ROM, the donor ROM or the balance references, and they cannot
 message the Overseer. So the job has three parts: a short prompt the Overseer
 writes and Ian pastes, the job itself under the rules below, and the
@@ -92,7 +92,7 @@
    bits and padding used, the divergence registrations, anything touched
    outside the job.
 2. Run `tools/oxide/merge-branch.sh cloud/<track>-<topic>`. It merges,
-   builds the merged tree on GitHub, runs the full gate on that ROM, and
+   builds the merged tree here, runs the full gate on that ROM, and
    pushes only on a pass. On a conflict it stops; resolve by hand, commit,
    and rerun with `--merged`.
    - The tracker conflicts most. Keep both sides' current entries, take the
@@ -106,5 +106,5 @@
    - Tell the balance track when scores go stale. A change to move data,
      the player's pool or the calculator needs a rescore before it merges,
      through a balance branch that carries both.
-   - Fetch a test-kit ROM if the job added kit entries, and update the
-     board.
+   - Build the test-kit ROM (`make testkit`) if the job added kit entries,
+     and update the board.
diff -ru a/.claude/skills/doc-links/SKILL.md b/.claude/skills/doc-links/SKILL.md
--- a/.claude/skills/doc-links/SKILL.md
+++ b/.claude/skills/doc-links/SKILL.md
@@ -61,9 +61,10 @@
 PYTHONPATH=. python3 -m tools.oxide.encounters.server
 ```
 
-The server on 8765 runs from the encounter tool builder's worktree, so after
-a landing that changes `server.py` it keeps the old code until that session
-restarts it; ask it to.
+The server on 8765 runs from `.claude/worktrees/ian-tool` (branch
+`ian-saves`), so after a landing that changes `server.py` it keeps the old
+code until it is restarted with `bash tools/oxide/encounters/restart_server.sh`
+(the `land-branch` skill, "After it lands").
 
 ## 4. Other sessions
 
diff -ru a/.claude/skills/oxide-session/SKILL.md b/.claude/skills/oxide-session/SKILL.md
--- a/.claude/skills/oxide-session/SKILL.md
+++ b/.claude/skills/oxide-session/SKILL.md
@@ -32,6 +32,8 @@
      the top of the tracker. Nothing else in the tracker.
    - The balance track: `docs/oxide/balance-plan.md`, and nothing in the
      tracker.
+   - The scoring track: `docs/oxide/trainer-scoring-handoff.md`, and nothing
+     in the tracker.
 4. On a worktree branch, run `git merge oxide` before anything else, resolve
    any conflict in your own files, and run your own suites. A branch cut before
    a change on `oxide` otherwise finds out only at the integration gate: the
@@ -99,7 +101,8 @@
    list with its "Why:" and "Unneeded if:". If this session changed something
    an entry rests on (hardware, a ruling, a dropped feature), update every
    entry, doc and memory resting on it in the same commit. If you are the encounter track, edit only your
-   one paragraph here; the balance track edits its plan instead.
+   one paragraph here; the balance and scoring tracks edit their own docs
+   instead.
 2. **Findings.** A durable fact learned this session (a correction, a defect, a
    measurement, a format detail) goes in the design doc's section 8 findings log,
    dated, and the design doc's version and date at the top are bumped. Status
@@ -137,8 +140,8 @@
 Delegate a task to a background general-purpose agent when it can run in
 parallel with other work, or when it is a long read (a catalogue, a survey, a
 batch of tables) whose detail this session does not need to hold; Ian has made
-that a standing preference. Do the rest inline. Ian's default model is Opus
-now, so a subagent no longer saves anything by being cheaper, and it starts
+that a standing preference. Do the rest inline. A subagent runs on the same
+model as this session, so it saves nothing by being cheaper, and it starts
 cold. Keep here anything that needs judgment across the project, anything in
 another track's files, and the report itself, since a subagent's report never
 reaches Ian. The brief has to carry everything:
diff -ru a/.claude/skills/playtest-day/SKILL.md b/.claude/skills/playtest-day/SKILL.md
--- a/.claude/skills/playtest-day/SKILL.md
+++ b/.claude/skills/playtest-day/SKILL.md
@@ -1,6 +1,6 @@
 ---
 name: playtest-day
-description: How to run a Platinum Oxide playtest session with Ian from docs/oxide/ingame-checklist.md, from fetching the right ROMs to recording each result as a tick or as an open bug. Use this whenever Ian says he is ready to play or test, the new CPU has arrived, a batch of in-game checks has piled up, or a session is asked to "go through the checks", even if he only names one check.
+description: How to run a Platinum Oxide playtest session with Ian from docs/oxide/ingame-checklist.md, from building the right ROMs to recording each result as a tick or as an open bug. Use this whenever Ian says he is ready to play or test, a batch of in-game checks has piled up, or a session is asked to "go through the checks", even if he only names one check.
 ---
 
 # A playtest day
diff -ru a/.claude/skills/read-donor/SKILL.md b/.claude/skills/read-donor/SKILL.md
--- a/.claude/skills/read-donor/SKILL.md
+++ b/.claude/skills/read-donor/SKILL.md
@@ -50,8 +50,7 @@
   through `donor.py` and the ROM anyway.
 - Learnsets are 34 fixed slots of (u16 move, u16 level); level 0 means an
   evolution move, which Platinum has no concept of and which imports as level 1.
-  Oxide's entry has been (u16 level, u16 move) since element 4, so the move id
-  is no longer capped at 511.
+  Oxide's entry is (u16 level, u16 move), so move ids above 511 fit.
 - Move battle effects share Platinum's numbering: 0 to 276 are Platinum's
   `BATTLE_EFFECT_*` in order and hg-engine's own run 277 to 406. The effect
   scripts come from hg-engine's source, not the ROM:
@@ -69,8 +68,7 @@
   (u16), 9 icon palettes (u8), 10 unidentified (u16, 26 non-zero; see the doc),
   11 form data (32 u16 per species, the personal indices of its forms), 12 and
   13 form-to-species and reversion. Hardlove's item table has 2,687 records;
-  element 7 brings a curated subset into Platinum's free slots, done on
-  `cloud/element7-items` and not yet merged.
+  element 7 brought a curated subset into Platinum's free slots (merged).
 - Encounter and trainer records encode forms as `(form << 11) | species`.
 - The form and alt-evolution slots on the pick-list (Alolan Ninetales 1132,
   Galarian Rapidash 1158, Gyarados M 1087, and the rest of that table) were
diff -ru a/CLAUDE.md b/CLAUDE.md
--- a/CLAUDE.md
+++ b/CLAUDE.md
@@ -103,13 +103,11 @@
 unmodified tree; `make rom` for an unchecked rebuild after edits. Output:
 `build/pokeplatinum.us.nds`.
 
-**The replacement CPU is in and passed its checks (2026-09-29).** The old
-i9-14900K was degraded: under all-core load, compilers and Python crashed or
-returned wrong answers (design doc findings log, 2026-09-22), and for a week
-every build ran on GitHub. The new chip ran the stress check that caught the
-old one with no failures, and built `oxide` from scratch twice on every core,
-matching GitHub's SHA-1 both times. Local builds and parallel jobs are back
-to normal, with no job limit.
+Builds run on this machine with no job limit, and a local ROM matches
+GitHub's build of the same commit byte for byte. Run any heavy or parallel
+job under `tools/oxide/capped`, which stops it at a memory cap rather than
+let it run WSL out of memory (the design doc's findings log has both
+histories: the degraded CPU of 2026-09-22 and the WSL crash of 2026-10-02).
 
 Hand Ian a ROM built here from a pushed commit whose ROM matches GitHub's
 SHA-1 for it, copied into `~/oxide-playtest` as
```

## Verifying

Every finding here is a stale fact or a conflict, checked against the
repository rather than by a behavioural probe: the tracker, `merge-branch.sh`,
the worktree list, `git blame` on the two doc-server passages, and the
constants headers. A session applying these hunks should rerun
`python3 tools/oxide/deferred_check.py` (the H6 rewrite adds no dated
deferral) and grep the skills for `fetch-rom`, `on GitHub` and `new CPU`
afterwards.

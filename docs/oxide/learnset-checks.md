# Learnsets by check and verify

Ian is dissatisfied with Oxide's learnsets and move balance (2026-10-06). Every
check on learnset v3 (on `balance-learngen-v2`, unlanded) was a rule about the
data, such as where Kaizo places a move or a power bar, and none measured how a
Pokemon plays. This plan improves the learnsets against checks that can be
run, the way the fight scorer was built: Ian's insights on a sample of lines
become general rules, and the result is verified on lines held back from the
generator. Ian approved the plan and asked for the baseline on 2026-10-06.

## The five steps

1. **Baseline** (now). Run the six checks below on oxide's learnsets and on
   v3's, so the first report also says whether v3 is better.
2. **Ian's insight sessions.** From the baseline, about 20 lines across the
   splits and roles (clear failures, borderline cases, and some that pass),
   which Ian judges as a player with his reasons. His rulings so far
   (`learnset-proposal-feedback` in memory, the standing rulings) are the
   starting rules.
3. **Five held out.** Five of the 20, drawn by a fixed seed, are never shown
   to the generator; they are the exam. Ian judges them last, after the rules
   from the other fifteen are locked, so his verdicts on them cannot shape
   the rules they test (a side agent's caution, kept by Ian, 2026-10-06).
4. **Extrapolate.** Ian's reasons become general rules or weights in the
   generator, never patches for one species, and it rewrites the 652 lists.
   Ian approved it on 2026-10-06; its brief is the last section below.
5. **Verify.** The generator reproduces Ian's verdicts on the five held-out
   lines, the six checks pass at his thresholds, and the bosses stay in their
   bands (the standing rulings' targets). A failure is understood, the rule
   adjusted, and the loop runs again.
   The first exam (2026-10-06) failed in part, and Ian sent the rewrite round
   a second loop the same day: each miss becomes a check over all 652 lists,
   the five lines are re-judged only to catch regressions, and the alpha run
   is the test on lines the rules were not built from. The boss bands are
   read in the goal 3 reading after the TM pass (alpha-readiness, step 15).

## The six checks

Each check reports oxide and v3 side by side: how many lines or moves pass,
how many fail, and the worst offenders by name. Thresholds are Ian's to set
after the baseline; the defaults below come from his rulings and are only
what the baseline reports against.

1. **A usable attack by the split's cap.** For every line the player can
   catch, at every stage it can reach by each split's cap from the split it
   is first caught in: an attack of its own type at 50 power or more, known
   at capture or learned by level-up by the cap. Ian's ruling (2026-09-27):
   no stage goes more than a split without one, except a stage the player can
   evolve by the end of Gardenia's split. What a Pokemon knows at capture is
   the last four moves its list gives by its catch level; relearner-only
   moves count for nothing (standing rulings). TMs are reported separately,
   since the TM pass has not placed them.
2. **A niche.** The scoring track's matchup screen (no simulated fights) run
   for every boss fight in the current trainer files on a few rolled boxes per
   split: a line passes when it is in the screen's top sixes for at least one
   boss in the split it is first caught in or the next. The report lists the
   lines no boss ever takes and the ones every boss takes, which Ian ruled are
   both signs of balance to fix (2026-10-02). The screen counts hits, so it
   cannot see a plan that wins on turns: it ranked the Mars 1 PP-stall six
   1,831st of 38,760, and only the race recovered it. So walls, stallers and
   support lines (Togetic, a Vullaby stall) may read as having no niche when
   they have one. Its "never taken" list is a lead to check with the race or
   a reading, not a verdict, and a flagged support line is never fixed just by
   giving it more attacks (a side agent's caution, kept by Ian, 2026-10-06).
3. **No dead moves and no universal ones.** From the same screen, how often
   each move is among the four the screen picks for a chosen Pokemon, totalled
   over all bosses. The screen picks moves by a fixed rule, so this shows what
   the screen values; full fight readings refine it as goal 3 proceeds.
4. **No early run-enders on the player's side.** Fixed-damage moves (Dragon
   Rage, Sonic Boom) and level-damage moves (Night Shade, Seismic Toss,
   Psywave) learnable before the end of Gardenia's split, and any one-hit KO
   move in a player list. Charmander's Dragon Rage out of Roark's split is
   ruled; the rest are flagged for Ian.
5. **Ian's standing move rules hold**, as a lint over the move and species
   data: every stat-raising setup move at 1 to 3 PP; the stat-lowering status
   moves at 3 to 6 (Sweet Scent 2, Defog 1, Memento as it is); no
   weather-setting move in any obtainable line's level-up, TM or tutor list,
   and no weather-setting or weather-cancelling ability in an obtainable
   line's regular slots; sleep moves, powders, Thunder Wave, Dark Void and
   Swagger at their Generation 4 accuracy; none of Ian's removed TMs on the TM
   list. Egg lists are trainer-only, so they are not player lists here.
6. **It reads right as a player.** One readable sheet per split: each capture
   area's catches, the catch level, the four moves known at capture, the
   level-up moves learned by the cap, and the stage at the cap, in the
   comb report's format (a table per area, every move named). This one is
   Ian's judgment, and the sheets are where step 2 picks its 20 lines.

## Who does what in the baseline

- **Checks 1, 4, 5 and 6**: a balance-track job on branch
  `balance-learnset-checks` (cut from `oxide`), as code in
  `tools/oxide/balance/learncheck.py` with a test, reading oxide's data from
  the tree and v3's from `origin/balance-learngen-v2`.
- **Checks 2 and 3**: the scoring track, which owns the matchup screen, run on
  both learnset versions.
- The report is `docs/oxide/learnset-baseline.md` on the balance branch, with
  the proposed 20 lines for step 2 (and which five are held out, sealed until
  step 5) at its end. The Overseer relays it to Ian.

## Step 4: the brief for the Balance Agent

Ian approved step 4 on 2026-10-06. It is the balance track's job, run by a
Balance Agent session at xhigh effort on its own branch,
`balance-learnset-rewrite`, cut from `oxide` in a worktree. The session reads
this section, the locked rules and the files named below, and nothing in the
exam.

**The exam stays sealed.** Never open, search or quote
`docs/oxide/learnset-exam.md`. The five held-out lines, named at the end of
`learnset-baseline.md`, get no special treatment: no patch, no exclusion, no
extra look. Step 5 is not this session's. The Overseer has the rewrite judged
against the exam by a reviewer who did not write the lists, and the Scoring
Agent reads the bosses on the branch against their bands.

**What to build on.**

- The locked rules and the utility tiers in `learnset-insights.md` ("The
  locked rules"), with the fifteen sessions above them as the reasons. R6 was
  narrowed after the lock (2026-10-06): a weaker move of the same type is
  dominated only when it has no secondary effect and is in the same physical
  or special class. Ian's reasons become general rules or weights, never a
  patch for one species.
- The standing rulings and the `balance-rules` skill, above all a move's worth
  at capture, every Pokemon's niche, the super-wanted lines, the weather rule,
  and egg lists as the trainers' palette only.
- `tools/oxide/balance/learncheck.py`, checks 1, 4, 5 and 6, and their
  baseline in `learnset-baseline.md`.
- Checks 2 and 3, the scoring track's matchup screen (`plniche.py`). Run it;
  do not edit it, since it is the scoring track's file. Its "never taken" list
  is a lead to check, not a verdict, and a support line is never fixed just by
  giving it more attacks (the caution under check 2 above).
- The v3 generator, `learnplan.py` and `laterlearn.py` on
  `origin/balance-learngen-v2`, as starting code if it helps. v3's lists
  failed as many stages as today's (51 each), so the work is new rules, not
  tuning.
- The tracker's move items: the move reworks, the rampage moves made
  one-turn, Sylveon unreachable, and Togepi and Togetic without an attack
  before 33.

**The work, in order.**

1. New checks in `learncheck.py`, numbered on from 7, each with a test and
   each reporting `oxide` and the rewrite side by side as checks 1 to 6 do:
   - R1, five or six usable moves by the first split's cap;
   - R2, two or three new moves per stage per split;
   - R4 and R5, the first coverage move by the second split, and the
     coverage count over the game;
   - R6, dominated moves, as narrowed;
   - R7, utility quality against the tier table;
   - R8, an evolution or learn-level choice that stays inside one split;
   - the other mechanical rules: R11, R21, R24 (Protect, Detect, Double Team,
     Ingrain and every one-hit KO move out of player lists), R25, R32, R37,
     and every evolution that needs a known move reachable by the player.
   Run them on `oxide` first and report that as the new baseline before
   writing any list.
2. Rewrite every level-up list, 652 of them, level-1 entries included, with a
   generator built on the locked rules. TM, tutor and egg lists are out of
   scope; the TM pass follows. The lists go into the game data on the branch
   (`res/pokemon/<species>/data.json`, through `tools/oxide/jsonstyle.py` or
   in the files' own style), so that the build, the checks and the scorer read
   them. Nothing lands until step 5 passes and Ian says yes.
3. The moves under review. Fury Attack and Feint leave player lists now. A
   move whose rework Ian has not ruled on (Fury Cutter, Psywave, Hyper Beam and
   the other two-turn attacks, the multi-hit moves) is not something a list
   relies on until he has. The rampage moves count only once they are one-turn
   (R9), so a list may place Thrash, Petal Dance and Outrage at their one-turn
   worth, and the report names every such placement as waiting on the engine
   change. A rework proposal Ian has to see (the multi-hit review, Uproar and
   Raging Fury) goes in the report as a question with its context.
4. Regenerate the check 6 sheets for the rewrite, so Ian can read it by split.

**Edit only** `tools/oxide/balance/` outside the scoring track's files
(`fightsim.py`, `fightai.py`, `perfectline.py`, the `pl*.py`, `pboxes.py`,
`pdoubles.py` and their tests), the learnsets in `res/pokemon/`,
`docs/oxide/balance-plan.md`, `docs/oxide/learnset-sheets/` and a new report,
`docs/oxide/learnset-rewrite.md`. Ask the Overseer before touching anything
else. Stage files by name.

**Done means**, each with its output in the report:

- every check, 1 to the last, run on `oxide` and on the branch, as a table of
  passes and failures with the worst offenders by name;
- `test_learncheck.py` and the balance suites pass;
- `make rom` builds the branch, and `bash tools/oxide/integrate.sh
  --verify-only` has no failures;
- the report lists failures and anything unverified first, then what waits on
  Ian (thresholds, rework questions), each question carrying its context.

Report to the Overseer with SendMessage ("Oxide Overseer") at each stage's
end: the new baseline, the rewrite, the report.

Ian's writing rules bind every line of the report, code comments and commit messages. The hard rules, from `~/.claude/CLAUDE.md`:

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

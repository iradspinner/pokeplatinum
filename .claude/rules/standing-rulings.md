# Standing rulings from Ian

A local session keeps these in its memory folder, which a cloud session cannot
read, so they are written here too. Each is a standing instruction.

- **Each change is judged for its effect on difficulty, by judgement.** Ian,
  2026-10-07: "this should dictate every single decision on every single
  agent." A change that does not materially move a fight's difficulty (a
  starter's level 5 moves, a TM's location, a line of dialogue) stales
  nothing and sets off no rescore or re-read; a material one names the
  fights it moves, and only those are marked for reading. Scores never block
  a landing: the gate reports stale scores and passes. No full reading is planned (Ian, 2026-10-29, dropping the
  milestone reading before alpha 1): the scorer reads only the fights Ian
  names, chiefly as a backup when a fight feels too hard in his testing,
  to show whether he is missing a line,
  and the simulator is frozen except for fixes he approves. The first scoring
  system's cheap estimate is retired (Ian, 2026-10-13): the scorer is the one
  measure of a fight. A problem Ian
  reports is fixed as data, with common sense, never turned into a standing
  rule, a generator rule or a gate check unless he asks for one. What counts
  as material is read from the fight's shape in `docs/oxide/boss-shapes.md`:
  a change to a boss's core, or to the player's core counterpiece to it, is
  material, and a change to a one-off Pokemon is not (Ian, 2026-10-12).
  Every landing commit says, in one line, "Difficulty: not material" or
  "Difficulty: material, <fights>". The rule exists because Roark's split
  was re-read more than 65 times before the alpha, and the full scorer costs
  60 to 75 hours a pass.
- Teams are designed by judgement with cheap checks, and the scorer only
  spot-checks (Ian, 2026-10-22: "the difference between a 94% WR and a 91%
  is honestly too low to be worth the time"). Tried first on Mars 1's dials
  and on Jupiter 1, whose sealed cheap-check prediction matched its reading
  on two boxes of three and missed the third by ten points on the hard side;
  Ian called it "good data and close enough" the same day, so it is the
  default for every fight. The checks underrate status and stall teams in
  long fights, so those get a margin, or a spot check when a box looks thin.
  A team change is checked by the speed tiers against the boxes' likely
  answers, the matchup screen, and the probe that the trainer AI uses each
  move, with Ian's judgement deciding; the scorer reads a fight only when
  Ian names it or a fight looks clearly off (the milestone reading before
  alpha 1 was dropped on 2026-10-29). A scorer gap is fixed only when it would change a
  decision, and the alpha playtest is the real measure of difficulty. The
  reason: a boss reading takes two and a half to four hours, iterating
  every boss through it is not workable, and each new modelling gap (the
  Flame Plate, the four moves carried between fights) put earlier numbers
  in doubt.
- Never launch an emulator. Ian runs melonDS on Windows and drives it; a local
  session attaches to it over the GDB stub (`debug-live` skill). A cloud
  session cannot reach it at all, so in-game checks are written into the
  tracker for Ian.
- A fix to a bug that is present in vanilla Platinum is its own commit, with
  "VANILLA FIX" in its subject, and is called out to Ian in the report,
  separately from fixes to Oxide's own bugs.
- No session owns files any more (Ian, 2026-10-13, retiring the track
  ownership of 2026-09-30 "for now, as the scope of changes we are making is
  much less than previously needed"): any session edits what a task needs and
  says in its commit what changed and why. The fight simulator, its AI and the
  scorer (`fightsim.py`, `fightai.py`, `perfectline.py`, the `pl*.py` modules)
  still change only with Ian's approval of each fix. If Ian starts several
  track sessions in parallel again, ask him whether ownership comes back.
  Ian approved, on 2026-10-14, every fix the verified gaps list
  (`docs/oxide/simulator-gaps.md`) names, so that fights are not rescored
  again and again: "fix everything except the Z and Max moves." Each fix
  still matches Oxide's engine, gets a test that fails before it, and lands
  through the Overseer; a new behaviour outside the list still needs his
  approval. The Z-moves and Max moves are not fixed and no player or
  trainer gets them; they were added by accident and are to be removed.
- A big review (a `/docs-pass`, a `/qa-pass`, a risky merge's review) goes to a
  helper the local session runs at xhigh effort with the Agent tool's effort
  setting, rather than asking Ian to switch (Ian, 2026-10-21); a routine
  helper may run at lower effort once he agrees to it for that job. The
  agent types in `.claude/agents` carry the settings: `big-review` at xhigh,
  and `lookup` on Haiku for read-only lookups (Ian's yes, 2026-10-21).
  Every helper runs as one of those types, never the general-purpose one,
  which inherits the Overseer's xhigh and was 82 percent of the usage (Ian,
  2026-10-21): `worker` (Opus at high) for the engine, the trainer AI, the
  simulator and scorer, and game data; `routine` (Sonnet at medium) for
  mechanical, fully specified jobs, such as regenerating a file, spelled-out
  doc edits and small tool fixes.
- The cloud code review (`/code-review ultra`) is never built into a procedure;
  run it only when Ian asks for it.
- Ian's user settings (`~/.claude/settings.json`) are his to edit. Hand him the
  exact change instead.
- Wild encounter tables follow the `author-table` skill: nuzlocke capture areas
  by location name, gym splits with Ian's level caps, a top share of about a
  third, and a question to Ian before padding a thin table. Swarm, Poke Radar
  and GBA dual-slot encounters are turned off and never go in a table (Ian,
  2026-09-26).
- Choice items are to be nearly entirely gone from Oxide (Ian, 2026-09-26,
  strengthening "rarer than in the base ROM" of 2026-09-23). A Choice-locked
  boss is weaker in play than its score: its AI picks a fixed move against a
  given lead, so the player chooses the lock and switches to something immune.
  The balance plan's item and trainer passes carry it. For the player it is
  absolute (Ian, 2026-09-27): no Life Orb and no Choice item is ever
  obtainable, and the best offensive items the player gets are the
  type-boosting ones (Charcoal, Mystic Water and the like).
- The local session named "Oxide Overseer" is the one standing session (Ian,
  2026-10-13): it keeps the tracker, the one home of open work, lands every
  branch on `oxide`, and coordinates in-game testing. Any other session Ian
  starts messages it with `SendMessage`; a cloud session cannot, so it reports
  through its branch instead (CLAUDE.md, "Cloud sessions").
- The player has no way to set, change or end weather for the whole game (Ian,
  2026-09-26): no weather move in any player learnset, TM, tutor or egg list,
  and no weather-setting or weather-cancelling ability in an obtainable
  Pokemon's regular slots. The exceptions are the game's single Ability Patch
  (exactly one exists), which may give a weather ability as a hidden ability,
  and Defog, which still clears fog. Trainers keep their weather. A weather
  ability found in an obtainable line's regular slot moves to its hidden slot
  (Ian, 2026-09-29: Psyduck, Snover, Hippopotas and Larvitar's lines), so
  trainers keep weather teams through hidden abilities, as Pelipper and
  Torkoal already do.
- Ian's super-wanted lines (the `wanted` list in
  `docs/oxide/encounters/values.json`) are never trimmed from the encounter
  tables, and a majority of them should be obtainable in a best-play run.
- Attrition lives in gauntlets (Ian, 2026-09-27): the Pocket PC heals, and
  works, everywhere except chosen one-way areas the player must clear, beating
  a set number of trainers in a row, before leaving to heal. Balance proposals
  that rely on route attrition belong in a gauntlet. A gauntlet is 2 to 5
  mandatory trainers on the easier side of average, counted without optional
  ones; bag items may heal between its fights (the danger is deaths
  snowballing); bosses stay outside it, with gauntlets leading up to them; and
  a majority of the game's trainers should be mandatory (Ian, 2026-09-27).
  How a gauntlet holds the player (Ian, 2026-09-29): only the way back is
  blocked, a one-way ledge at the entrance where the map allows, so the
  player cannot retreat to heal but may push on past a trainer; while a
  section is open the Pocket PC, the Escape Rope and Dig refuse.
- Evolution stones are deliberately scarce (Ian, 2026-09-27): two lines
  competing for one stone is intended, because it weakens the box and makes
  the player choose (with one Sun Stone, an Eevee and a Charcadet owner picks a
  different Eeveelution). Do not add stones just to settle a contest; the
  balance track's stone census is where the counts are set.
- Move numbers follow the later games, priority included, and the base
  ROM's own values stay (Ian, 2026-09-26 and 27). Setup stays expensive:
  every stat-raising setup move at 1 to 3 PP and the stat-lowering status
  moves at 3 to 6, for any move added later too (2026-10-02). Sleep moves,
  powders, Thunder Wave, Dark Void and Swagger keep their Generation 4
  accuracy, and Kaizo's changes come in only as `docs/oxide/kaizo-comparison.md`
  lists. The move reworks of 2026-10-06 (the rampage moves one turn with
  recoil, the recharge moves without recharge, one two-to-five-hit move per
  type at 25 a hit, and the rest) are listed in full in
  `docs/oxide/rulings-detail.md`; read it before changing a move.
- A doc Ian is pointed at gets a clickable link that opens it rendered in his
  browser, never a bare path (Ian, 2026-09-27): the OxiDex's viewer at
  `http://localhost:8765/doc/<path>` (with `?ref=<branch>` for an unmerged
  branch), or the GitHub page of the pushed branch. The `doc-links` skill has
  the forms.
- A move's worth to the player is what the Pokemon knows at capture (the last
  four moves its list gives by its level, which can include moves below the
  catch level) plus what it learns by level-up afterwards (Ian, 2026-09-27).
  Relearner-only moves, an evolved form's level-1 moves among them, count for
  almost nothing: the relearner is in Pastoria, each move costs a scarce Heart
  Scale, and each use competes with every other in the box. Level-1 lists
  matter as the relearner's menu and the legal palette for trainer teams.
- A level-up list may take any working move in Oxide that fits the line;
  later games' lists are inspiration, not pick lists (Ian, 2026-10-06). A
  move meant only for trainers never lands in a wild catch's four, two
  branches of one line are close in worth where the player chooses between
  them, a strong move below a line's catch level moves to or after it, and
  Eevee's evolutions each learn a full moveset from 20. The generator's
  narrowings for alpha 1's rewrite are in `docs/oxide/rulings-detail.md`.
- Local builds are trusted (2026-09-29): a ROM goes to Ian as soon as the
  local gate passes. Matching GitHub's SHA-1 first was a guard against the
  degraded CPU and is no longer required (Ian, 2026-10-06); GitHub's build
  is retired (2026-10-28), so a build that looks wrong is rebuilt clean here.
- How the fight scorer reads a fight (Ian, from 2026-09-30): its job is to
  order every fight by difficulty, and close enough is good enough while the
  order is broadly right. A fight is judged on its win rate, its average
  faints and its clean rate together, win rate first; its one difficulty
  number is average faints plus 40 times its losing rate. Fights are played
  at the game's real odds, beside a very unlucky stress test. A boss gets a
  six the scorer chooses over a spread of goal 3's boxes; an ordinary
  trainer is read blind from the box's stronger half. Targets: an ordinary
  trainer won cleanly 80 to 85 percent of the time, no boss above 95 percent
  won (the Galactic officers may near 100 so long as their death rate is
  not trivial, and none reads harder than its commander, Hesperid likely
  excepted; 2026-10-21), the hardest bosses near 80. The
  scorer's good play must arise from search over the real simulator, never
  from named rules. Since 2026-10-22 it only spot-checks (the second ruling
  above). The full ruling, with the held-back versions, the box rules, the
  soft guides and the boss level rules, is in `docs/oxide/rulings-detail.md`;
  read it before running or changing the scorer.
- A loss of any kind ends the whole run (Ian, 2026-09-28): there are no second
  attempts, at a boss or anywhere. The one exception is the first battle with
  Barry on Route 201 (Ian, 2026-10-02): it does not count for deaths or
  wiping, and can be ignored, as the game itself lets it be lost. Every fight is scored and designed as a
  first and only attempt; a boss's planned team comes from knowing the fight
  in advance, never from an earlier loss.
- Every Pokemon in the game should have an important niche at the point the
  player has it, while it stays fine for some lines to be stronger than
  others (Ian, 2026-09-28). Garchomp outvalues Furret, but only one of them
  can carry Gardenia's split; Mamoswine outvalues Aggron late, yet Aggron is
  one of the best physical walls. Ian's super-wanted lines sit marginally
  above average, a personal bias. The encounter tool's tiers are availability
  labels only, not intended power.
- TMs are single-use again, as in vanilla (Ian, 2026-09-28): each placement
  gives a set number of copies (strong TMs one, utility ones two or three).
  Weak TMs are not sold; the TMs the Veilstone Department Store and the Game
  Corner do sell unlock by badge count in order of usefulness, and each can
  be bought once, like any other placement (Ian, 2026-10-06); each is the reward for beating one optional trainer
  of weak-to-medium strength near its split. About 100 TMs. Ian's removals:
  Protect, Double Team, the four weather moves, Thief, Snatch, Skill Swap,
  Focus Punch, Substitute, Dream Eater, Swords Dance and Embargo; Toxic,
  Will-O-Wisp and status of Thunder Wave's reliability may be TMs only as
  single copies. Since field moves work on the badge alone (2026-09-29;
  Surf also waits on Cyrus beaten at Celestic Town, Ian, 2026-10-31, so the
  water cannot skip Celestic's story), the
  HMs are single-use TMs too, less Cut and Rock Smash (the TM list of
  2026-10-06), and Fly, Strength, Defog and Rock Climb need buffs to earn a
  place. Egg move lists serve only as trainer teams' palette: a
  nuzlocke has no breeding.
- A change that moves what the save stores costs Ian a fresh start, not a
  save converter (Ian, 2026-09-28, on element 7's bigger Bag): he starts a
  new game on the first ROM with the change, and again after each later
  one (the TM pass's Bag growth, 30 boxes). Tell him before the landing
  which ROM starts the new game, and keep the OxiDex's save reader in step.
- No GitHub Actions in the private repos (`oxide-rom-builder`,
  `melonDS-oxide`), for good (Ian, 2026-10-01, ending the pause of
  2026-09-29). Every ROM is built locally and landed with `merge-branch.sh`;
  the private ROM builder and `fetch-rom` are retired; the melonDS fork is
  built on Ian's PC with MSYS2 (since 2026-10-06). The public repo's ROM
  build is retired too (Ian, 2026-10-28: "local builds are enough"), after
  the account's free Actions ran out on 2026-10-07; its workflow is
  disabled on GitHub and deleted from the repo.
- An instruction to act on a later day, or once something happens (Ian,
  2026-10-01), lives only in the tracker's Scheduled list, with why it exists
  and what would make it unneeded; other docs point at it. Before acting on
  an entry, a session checks its reason against today's state and asks Ian if
  it no longer holds. A session that changes a premise (new hardware, a
  reversed ruling, a dropped feature) updates every entry and note resting on
  it in the same commit. `tools/oxide/deferred_check.py`, run by the gate,
  refuses an entry without its reason, an entry past due, and a dated
  deferral anywhere else. The rule exists because on 2026-10-01 the Overseer
  switched two workflows back on from a dated note, though the new CPU had
  made one of them unnecessary.
- When the permission check refuses an action a task needs, the session stops
  the task and tells Ian what was refused and why it was needed, and never
  works around it (Ian, 2026-10-01). A cloud session says so in its branch's
  last commit.
- New held items go behind optional challenges, not in shops (Ian,
  2026-09-29): element 7's held items (Eviolite, Assault Vest, Rocky Helmet
  and the rest) are each placed as the reward for an optional trainer, a
  spinner the player can choose to walk into, or another optional fight,
  rather than sold, even though a shop with a set price would be simpler.
  The item pass places them; the balance census counts each from its
  fight's split. A trainer's reward, held item or TM, is given
  automatically straight after the player wins, not on talking to the
  trainer again (Ian, 2026-10-06, relayed by the main track). The Game
  Corner's vanilla held items (Silk Scarf, Wide Lens, Zoom Lens, Metronome)
  move behind optional fights the same way (Ian, 2026-10-06).
  The Game Corner's gift for ten straight slot bonus rounds, pure luck,
  becomes the reward for beating an optional trainer there (Ian, 2026-10-06).
  The Game Corner sells no Heart Scales or PP Ups; its prizes are its gated
  TMs and what else it sold before (Ian, 2026-10-06).
- Anything drawn from Platinum Kaizo's data (teams, learnsets, items, sets)
  is translated twice: extrapolated into Oxide's Generation 5+ moves,
  abilities and items, as Kaizo would have built with the modern pool, and
  scaled to Oxide's easier difficulty. Tools have repeatedly done only the
  second (Ian, 2026-10-07); a brief that hands over Kaizo data names both,
  with a check for the first. The comb's brief is unchanged for now.
- Trainer design at about 6/10 of Platinum Kaizo (Ian, from 2026-09-29):
  bosses keep Kaizo's structure at reduced lethality; an ordinary trainer
  carries one idea, is genuinely dangerous, and has 3 to 5 Pokemon (6 from
  Gardenia's split on), sizes varying. No one-hit KO move on any trainer;
  evasion and trapping are rare; a boss carries at most one forced trade
  (none before Fantina) and an ordinary trainer none, though from Wake's
  split on an ordinary trainer may occasionally carry Self-Destruct,
  Explosion or Destiny Bond, or trapping (Ian, 2026-10-31: "at this point
  in the game they are occasionally acceptable"). Every enemy Pokemon
  holds its own item and has its own nature, with no repeats in a team
  (2026-10-12). Trainers may use TM and tutor moves freely, and from Cyrus
  3's split on any move. A move on a team Ian builds that its species
  cannot have at that level goes on the line's first-stage egg list
  without asking him, and a level-up list never moves for it
  (2026-10-29). Boss levels spike by importance: leaders, rivals,
  Cyrus and the League keep their aces at the cap, officers and the other
  mini-bosses sit 2 to 4 under it, and the Elite Four's aces run from 72 to
  78. The named Galactic fights are mostly anything goes, so long as each is
  fun and thematic. Ian plans a boss by baiting matchups in the order he
  wants, and a lead may be wholly countered by a Pokemon or a type when
  that answer draws in a member that beats it with a setup move, since
  the player's switch then hands it a free turn (2026-10-29). A split
  carries 10 to 15 mandatory non-boss fights, gym trainers not counted,
  and a trainer who turns, spins or walks counts as optional and may be
  harder than normal (2026-10-29). Two trainers the player fights alone
  together field six Pokemon between them at most, barring Ian's
  explicit permission (2026-10-29). Ordinary trainers favour variety over
  the optimal: neutral or less common natures more often, items that are
  not the textbook pick (2026-10-29). The full ruling (luck items, Focus Sash, Custap and enemy priority,
  accuracy, conditional moves, members under their evolution level, the
  iv_scale) is in `docs/oxide/rulings-detail.md`; read it before designing a
  team.
- Level caps are soft (Ian, 2026-10-29): experience and Rare Candies pass
  the cap, and the player's honour keeps an over-cap Pokemon out of fights
  (it may finish the fight it went over in, then is boxed until a later cap
  covers it; inside a gauntlet section it sits out the rest). The OxiDex
  flags over-cap party members; the game shows nothing; the Day Care is not
  considered. Mini-bosses get honour caps of their own, their aces at those
  caps. Ordinary trainers climb in level through a split, never reaching
  the cap and very rarely one under it, with harder sets at lower levels,
  split by split as each is worked; a mid-split ordinary fight's box rides
  the line of the cap less the split's experience still to come, once Ian
  approves the scorer's method. The full ruling is in
  `docs/oxide/rulings-detail.md`.
- Reports to Ian are one page (Ian, 2026-10-06). Any report, reading,
  study result or plan that comes to him starts with a one-page summary: the
  outcome, the action items (what he decides or does), the next steps, and
  how long each step will take. The detail goes below that summary or in a
  reference doc, which he does not read in full; the trainer-scoring
  handoff, at its length, is unreadable for him. The tracker's first page is
  that one page for the whole project (Ian, 2026-10-13).
- Prefer judging each Pokemon over global hard rules (Ian, 2026-10-06):
  "It entirely depends on the pokemon, and keeping it to hard rules destroys
  the variability between pokemon... We need to stop creating this web of
  hard rules that gets us into bad spots like this." A rule that flattens the
  differences between lines is a defect. For learnsets, a gap is filled from
  the rung of the type's move ladder (every working move of that type, by
  power and effect) that fits the point in the game and the Pokemon, climbing
  a rung or two a split, never by taking the strongest move a ceiling allows;
  Giga Drain is far too strong for Roark's split. Pivoting moves (Flip Turn,
  U-turn, Volt Switch and the like) are high rungs, never early first moves,
  since pivoting is very strong; and a line's ability can set its side of
  the ladder (Huge Power makes Marill a physical attacker) (Ian, 2026-10-06).
- Every trainer team in the finished ROM is set by hand (Ian, 2026-09-27):
  no trainer keeps default moves, so default movesets carry no weight in any
  argument, about learnsets, level-1 order or anything else.
- Frame work as checks (Ian, 2026-10-06). AI work is best at tasks it can
  verify and improve against that verification, and Ian's requests are often
  not phrased that way. Before starting an open-ended request or project,
  restate it to him as a short list of pass/fail checks, each saying how it
  is verified (by the session alone, or by Ian in game with the session
  reading the result), which pass today, and what he must decide; prompt him
  to reword or rework the request into that form. Run the cheap checks first,
  and claim nothing as done, fixed or passing without the output in hand
  (Ian, 2026-10-06, from the superpowers plugin's verification skill).

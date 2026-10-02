# Standing rulings from Ian

A local session keeps these in its memory folder, which a cloud session cannot
read, so they are written here too. Each is a standing instruction.

- Never launch an emulator. Ian runs melonDS on Windows and drives it; a local
  session attaches to it over the GDB stub (`debug-live` skill). A cloud
  session cannot reach it at all, so in-game checks are written into the
  tracker for Ian.
- A fix to a bug that is present in vanilla Platinum is its own commit, with
  "VANILLA FIX" in its subject, and is called out to Ian in the report,
  separately from fixes to Oxide's own bugs.
- Before editing a file another track owns, stop and say so: which files, whose
  track, and the choice of handing it over or taking it on with Ian's say-so.
  The encounter track owns `tools/oxide/encounters/`, `res/field/encounters/`,
  `docs/oxide/encounters/`, the `encounter-*.md` docs and one paragraph at the
  top of the tracker. The balance track owns `tools/oxide/balance/` and
  `docs/oxide/balance-plan.md`, except the fight simulator, its AI and the
  perfect-line scorer in that folder (`fightsim.py`, `fightai.py`,
  `perfectline.py`, the `pl*.py`, `pboxes.py` and `pdoubles.py` modules, their
  tests and results), which the scoring track owns with
  `docs/oxide/trainer-scoring-handoff.md` (Ian, 2026-09-30).
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
- Several sessions work at once, and a local session named "Oxide Overseer"
  coordinates them: the docs outside each track's own files, pushes to
  `oxide`, merges, and in-game testing. A local session messages it with
  `SendMessage`. A cloud session cannot, so it reports through its branch
  instead (CLAUDE.md, "Cloud sessions").
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
- Move numbers follow the later games (Ian, 2026-09-26, the staples survey's
  answer 1), priority included (2026-09-27), and the base ROM's own values
  stay. Setup stays expensive: every stat-raising setup move is at 1 to 3 PP,
  and the stat-lowering status moves at 3 to 6 (Sweet Scent 2), which applies
  to any move added later too. Sleep moves, powders, Thunder Wave, Dark Void
  and Swagger keep their Generation 4 accuracy. Kaizo's changes come in only
  as `docs/oxide/kaizo-comparison.md` lists (Ian's answers, 2026-09-27).
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
- The replacement CPU is in and passed its stress and build checks
  (2026-09-29), so the three-job limit of 2026-09-27 is lifted and local
  builds are trusted: a ROM counts when its SHA-1 matches GitHub's build of
  the same commit.
- How the fight scorer reads a fight (Ian, 2026-09-30, on the trainer-scoring
  handoff). The aim is to beat the game: a win that loses a Pokemon is still a
  win, but each loss takes away later team-building options. Lines are ranked
  by win rate first and average faints second (Ian, 2026-10-02, refining
  "clean wins come first"): a line that always wins with one sacrifice beats
  one that wins cleanly nine times in ten and loses the tenth, since one
  unlucky turn there ends the run. Options that win about equally often (within
  the estimate's noise) are then ranked by fewest faints; the clean rate is
  reported, not optimised. A boss is read
  over a spread of rolled boxes, so that its answers do not narrow to one
  Pokemon. Ties between equal AI picks break at random. Every fight is
  simulated at the game's real odds, with no luck budget (Ian, 2026-10-02,
  replacing the budget of 2026-09-30, under which every secondary status
  against the player landed and one crit could): the three numbers are then
  true frequencies with bad luck inside them, and the planner's caution
  comes from how heavily a position values a faint, weighing each chance at
  its true odds. The stress test that replaces the budget (Ian, 2026-10-02)
  replays the chosen line at disadvantage: every status and crit check, the
  trainer's and the player's, rolls twice and keeps the result worse for the
  player (the trainer's 1-in-24 crit lands about 1 in 12 and a 10% status
  about 19%; the player's own crits and secondary effects land less often,
  and its full-paralysis and confusion checks go against it). Its three
  numbers are reported beside the real-odds ones, as a very unlucky fight.
  Each trainer is read on 100 simulated fights: 75 at real odds and 25 very
  unlucky (Ian, 2026-10-02, replacing 200 of each as too costly). When a fight reads too hard, the player's move pools are the first
  candidate for change, since they are sparse in interesting options and lack
  many modern moves. A fight is judged on three numbers read together, never
  the clean rate alone (Ian, 2026-10-01): the clean rate, the share of
  simulated fights won with no Pokemon fainting; the win rate, the share won
  at all (no wipe); and the death count, the average number of the player's
  Pokemon that faint per simulated fight, which separates the hardest fights
  (Gardenia, Wake, Cyrus 3, Cynthia) where few runs win cleanly. The
  scorer's good play must arise on its own (Ian, 2026-10-01): it decides
  turn by turn by simulating its options in the real simulator against the
  exactly known trainer AI, and values a position by its state (HP,
  survivors, items, weather turns, PP, stat stages). A play it misses is
  fixed in that general machinery, never by adding a named behaviour, since
  a scorer that plays only what its rules name would need a rule for every
  team in the game. The planning ideas of the three-gym run are its exam,
  not its rules.
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
  Weak TMs are not sold; each is the reward for beating one optional trainer
  of weak-to-medium strength near its split. About 100 TMs. Ian's removals:
  Protect, Double Team, the four weather moves, Thief, Snatch, Skill Swap,
  Focus Punch, Substitute, Dream Eater, Swords Dance and Embargo; Toxic,
  Will-O-Wisp and status of Thunder Wave's reliability may be TMs only as
  single copies. Once field moves work on the badge alone, the HMs become
  single-use TMs too, and Fly, Strength, Defog and Rock Climb need buffs to
  earn a place. Egg move lists serve only as trainer teams' palette: a
  nuzlocke has no breeding.
- A change that moves what the save stores costs Ian a fresh start, not a
  save converter (Ian, 2026-09-28, on element 7's bigger Bag): he starts a
  new game on the first ROM with the change, and again after each later
  one (the TM pass's Bag growth, 30 boxes). Tell him before the landing
  which ROM starts the new game, and keep the OxiDex's save reader in step.
- No GitHub Actions in the private repos (`oxide-rom-builder`,
  `melonDS-oxide`), for good (Ian, 2026-10-01, ending the pause of
  2026-09-29). Every ROM is built locally and landed with `merge-branch.sh`;
  the private ROM builder and `fetch-rom` are retired; the melonDS fork is to
  be built on Ian's PC with MSYS2. The public repo's build on a push to
  `oxide` is free and stays on, and gives the SHA-1 to compare with.
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
  fight's split.
- Trainer design at about 6/10 of Platinum Kaizo (Ian's answers to the Kaizo
  team study, 2026-09-29). Bosses keep Kaizo's structure at reduced
  lethality; an ordinary trainer carries one idea. One-hit KO moves never go
  on a trainer, and evasion setups are rare. Trapping (the abilities, Mean
  Look or Block with Perish Song, the binding moves) is allowed but rare. A
  boss carries at most one forced trade (Explosion, Self-Destruct, Destiny
  Bond), none before Fantina, never made certain by Custap or priority, and
  an ordinary trainer carries none. No level-1 Focus Sash and Endeavor sets.
  No overlevelled optional trainers. Oxide adds some double battles. Teams
  are judged against Oxide's box, not Kaizo's. Ian plans a boss by baiting
  matchups in the order he wants, so the main tax on him is moveset overlap
  and coverage, then switching or staying in by fight.
- Every trainer team in the finished ROM is set by hand (Ian, 2026-09-27):
  no trainer keeps default moves, so default movesets carry no weight in any
  argument, about learnsets, level-1 order or anything else.

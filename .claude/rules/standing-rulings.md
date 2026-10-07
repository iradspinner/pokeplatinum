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
  and the stat-lowering status moves at 3 to 6 (Sweet Scent 2, Defog 1,
  Memento left as it is; Ian, 2026-10-02), which applies to any move added
  later too. Sleep moves, powders, Thunder Wave, Dark Void
  and Swagger keep their Generation 4 accuracy. Kaizo's changes come in only
  as `docs/oxide/kaizo-comparison.md` lists (Ian's answers, 2026-09-27).
  The rampage moves become one-turn moves, since a two- or three-turn lock
  is too dangerous in a permadeath run (Ian, 2026-10-06): Thrash, Petal
  Dance and Outrage take Kaizo's versions (Thrash 120 with a 20% paralysis
  chance and a third of the damage as recoil; Petal Dance 100 with a 20%
  confusion chance; Outrage 140 with half as recoil), and Uproar and Raging
  Fury, which Kaizo lacks, get one-turn versions on the same pattern.
  The other move reworks, as the learnset rewrite's report recommended
  (Ian, 2026-10-06): Hyper Beam, Giga Impact, Rock Wrecker and Roar of
  Time at 180, 100%, no recharge, half the damage as recoil; Blast Burn,
  Frenzy Plant and Hydro Cannon without recharge, at 95% with Kaizo's
  recoil and status; Sky Attack one turn (120, a third as recoil, 20%
  paralysis); Dig 60 and Dive 80 one turn; Fly, Bounce, Phantom Force and
  Shadow Force kept two-turn; every two-to-five-hit move at 25 a hit;
  Fury Cutter as Kaizo's three rising hits; Psywave cut for Psybeam;
  Spite at 5 PP; Uproar one turn at 100 with 20% confusion; Raging Fury
  one turn at 120 with a third as recoil and 20% confusion.
  Later the same day: one two-to-five-hit move per type. Normal keeps Fury
  Swipes and Cinccino's Tail Slap; Double Slap, Comet Punch, Barrage and
  Spike Cannon leave the game, their learners taking Fury Swipes or their
  own type's multi-hit move; Bone Rush goes to 100%. The trainer AI rates a
  multi-hit move on its expected hits (about 3.1, or 5 with Skill Link).
  Uproar and Raging Fury hit one chosen foe.
  Poison Fang takes Kaizo's 90 power and 40% chance to badly poison (Ian,
  2026-10-06).
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
- A level-up list may take any working move in Oxide that fits the line
  (Ian, 2026-10-06, relayed by the balance track): "You should look at the
  total pool of available moves for possible additions; future gen
  learnsets (either via hg-engine or via looking them up) should be used as
  inspiration, not as pick lists." A move a later game, Generation 4 or
  Kaizo gives the line weighs in its favour; its absence there does not
  rule it out. For alpha 1's rewrite Ian accepted two narrowings of the
  generator (2026-10-06): a status move it adds must already be linked to
  the line (canon, Kaizo or Oxide's lists), an unlinked attack comes in only
  to fill a gap a rule asks for, and the attacks and utility moves it adds
  keep under per-split ceilings, his answer 8 of 2026-09-27 (no ceiling on
  coverage power) set aside for this pass.
  From the learnset exam (Ian, 2026-10-06): a move meant only for trainers
  never lands in a wild catch's four (it goes on the egg list, the trainers'
  palette); two branches of one line are close in worth at the split where
  the player chooses between them; a strong move below a line's catch level
  moves to or after it; and Eevee's evolutions are the exception to the
  stone rule's late, sparse lists, each learning a full moveset from 20, the
  level Bebe's Eevee is held at.
- Local builds are trusted (2026-09-29): a ROM goes to Ian as soon as the
  local gate passes. Matching GitHub's SHA-1 first was a guard against the
  degraded CPU and is no longer required (Ian, 2026-10-06); it comes back
  only if a build ever looks wrong.
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
  simulated at the game's real odds, with no luck budget (Ian, 2026-10-02):
  the three numbers are then
  true frequencies with bad luck inside them, and the planner's caution
  comes from how heavily a position values a faint, weighing each chance at
  its true odds. The stress test that replaces the budget (Ian, 2026-10-02)
  replays the chosen line at disadvantage: every status and crit check, the
  trainer's and the player's, rolls twice and keeps the result worse for the
  player (the trainer's 1-in-24 crit lands about 1 in 12 and a 10% status
  about 19%; the player's own crits and secondary effects land less often,
  and its full-paralysis and confusion checks go against it). Quick Claw
  and Focus Band roll against the player too (Ian, 2026-10-06). Its three
  numbers are reported beside the real-odds ones, as a very unlucky fight.
  Each trainer is read on 100 simulated fights: 75 at real odds and 25 very
  unlucky (Ian, 2026-10-02, replacing 200 of each as too costly). A fight's
  single difficulty number, shown in the OxiDex's Trainers tab, is its
  average faints plus 40 times its losing rate at real odds (Ian,
  2026-10-07, relayed by the encounter track). The
  scorer's job is to order every fight in the game correctly by difficulty;
  it need not win as a person would, and close enough is good enough while
  that order is broadly right (Ian, 2026-10-02). For a boss the scorer
  chooses the six and their moves itself, in three stages: a screen by
  matchups with no simulated fights, a race among the screen's best sixes,
  and the full reading of the two or three left (Ian, 2026-10-02). The
  play-out planner runs at budget 64, and finalists whose win rates lie
  within 5 points count as equal before faints decide (Ian, 2026-10-03).
  An ordinary trainer is read blind: each simulated fight draws a random six
  from the stronger half of the box, never one held below the cap (Ian,
  2026-10-04). Targets (Ian, 2026-10-04): an ordinary trainer is won cleanly
  80 to 85 percent of the time (replacing the provisional 70 to 80); no boss
  reads above 95 percent won; a boss's difficulty spikes or drops with how
  important it is, and Oxide's hardest bosses top out around the easiest of
  Kaizo's read on the same box (about 80 percent won). The numbers order
  fights rather than measure them absolutely, and Oxide is not meant to be
  beaten on a first run. A trainer that trends a little hard, or reads as an
  outlier, is fine while it approximates its band (Ian, 2026-10-06).
  Cyrus 3, the biggest boss but Cynthia, may read harder than the rest
  (Ian, 2026-10-06: "if any fight can be excused for being too hard, the
  biggest boss fight of the game (save Cynthia) surely has that claim").
  From about Cyrus 3 on, a boss may carry two or three legendaries where its
  team needs them, against one before (Ian, 2026-10-06).
  Boss levels spike by importance (Ian, 2026-10-06): gym leaders, rivals,
  Cyrus and the League keep their aces at the cap, while officers and the
  other mini-bosses sit a few levels under it and earn their difficulty
  from sharper sets. Cyrus 3 is today's team raised to the cap's levels.
  Across
  the spread of boxes it reports which encounters its sixes always take and
  which they never take, since both mark encounter balance to work on (Ian,
  2026-10-02). When a fight reads too hard, the player's move pools are the first
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
  Weak TMs are not sold; the TMs the Veilstone Department Store and the Game
  Corner do sell unlock by badge count in order of usefulness, and each can
  be bought once, like any other placement (Ian, 2026-10-06); each is the reward for beating one optional trainer
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
  the private ROM builder and `fetch-rom` are retired; the melonDS fork is
  built on Ian's PC with MSYS2 (since 2026-10-06). The public repo's build on a push to
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
  fight's split. A trainer's reward, held item or TM, is given
  automatically straight after the player wins, not on talking to the
  trainer again (Ian, 2026-10-06, relayed by the main track). The Game
  Corner's vanilla held items (Silk Scarf, Wide Lens, Zoom Lens, Metronome)
  move behind optional fights the same way (Ian, 2026-10-06).
  The Game Corner's gift for ten straight slot bonus rounds, pure luck,
  becomes the reward for beating an optional trainer there (Ian, 2026-10-06).
  The Game Corner sells no Heart Scales or PP Ups; its prizes are its gated
  TMs and what else it sold before (Ian, 2026-10-06).
- Trainer design at about 6/10 of Platinum Kaizo (Ian's answers to the Kaizo
  team study, 2026-09-29). Bosses keep Kaizo's structure at reduced
  lethality; an ordinary trainer carries one idea. One-hit KO moves never go
  on a trainer, and evasion setups are rare. Trapping (the abilities, Mean
  Look or Block with Perish Song, the binding moves) is allowed but rare. A
  boss carries at most one forced trade (Explosion, Self-Destruct, Destiny
  Bond), none before Fantina, and an ordinary trainer carries none. Custap
  Berry and enemy priority are fair tools beside a trade: the player plays
  around Custap with their own priority, and enemy priority is part of
  planning (Ian, 2026-10-06, dropping the earlier "never made certain by
  Custap or priority"). The 90 percent accuracy bar of the learnset rules
  (R37) is for the player's movesets only, since the player plans around
  low accuracy; trainers are welcome to moves like Sing and Zap Cannon (Ian,
  2026-10-06). Luck items are allowed on trainers: Quick Claw, Focus Band,
  King's Rock, Razor Fang and the like, his own teams' Quick Claws included
  (Ian, 2026-10-06); the evasion items (BrightPowder, Lax Incense) stay
  under the evasion-is-rare rule. A Focus Sash may go on a lead that carries
  the boss's trade (Ian, 2026-10-06). No level-1 Focus Sash and Endeavor sets.
  No overlevelled optional trainers. Oxide adds some double battles. An
  ordinary trainer carries 3 to 5 Pokemon (6 is fine from Gardenia's split
  on), team sizes vary from fight to fight, and ordinary trainers are
  genuinely dangerous: two-Pokemon teams are too trivial (Ian, 2026-10-04).
  Trainers may use TM and tutor moves freely (Ian, 2026-10-04). A move cut
  from the TM list for the player's sake stays in the trainer palette of
  every species that learned it by TM before the TM pass, as egg moves do,
  and from Cyrus 3's split (Galactic) on a trainer's move need not be legal
  for the species at all: late teams are "basically no holds barred" (Ian,
  2026-10-07; the Overseer set the line at that split). Protect,
  Detect, Double Team and every one-hit KO move leave every player-accessible list,
  level-up, TM and tutor alike, and the one-hit KO moves leave every
  moveset or become other moves (Ian, 2026-10-06). Teams
  are judged against Oxide's box, not Kaizo's. Ian plans a boss by baiting
  matchups in the order he wants, so the main tax on him is moveset overlap
  and coverage, then switching or staying in by fight.
- Reports to Ian are one page (Ian, 2026-10-06). Any report, reading,
  study result or plan that comes to him starts with a one-page summary: the
  outcome, the action items (what he decides or does), the next steps, and
  how long each step will take. The detail goes below that summary or in the
  track's own doc, which he does not read in full; the trainer-scoring
  handoff, at its length, is unreadable for him. A track's status home may
  stay long, as long as its summary is kept current at its top.
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

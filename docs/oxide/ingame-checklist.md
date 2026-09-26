# Platinum Oxide: the in-game checklist

Every check that waits on Ian playing the game, in one place and in the order a
playtest day meets them (Ian, 2026-09-26: all at once when the new CPU is in).
The tracker's "Waiting on Ian" points here; this file holds the full wording.
The `playtest-day` skill runs the day from it. When a check passes, tick it and
move it to the bottom section with the date; when it fails, it becomes an
"Open bug" entry under the tracker's Phase 5, and the line here says so.

Checks marked **(live)** need a local agent attached to melonDS over the GDB stub
(the `debug-live` skill). Ian drives; the agent reads memory. Nothing here asks
an agent to launch an emulator.

## 0. Before anything: the new CPU

The i9-14900K is degraded (design doc findings log, 2026-09-22) and its
replacement is on the way. When the new chip is in, and before any playtest:

- [ ] Delete the venv block in the `Makefile`, the build retry in
  `integrate.sh`, the wedge guard (its rule in `.claude/hooks/oxide_guard.py`,
  `wedge_status.sh` and its test beside it, and the `statusLine` entry in
  `~/.claude/settings.json`, which Ian edits himself), the local-build rule in
  `.claude/hooks/oxide_guard.py` that refuses full builds, its paragraph in
  CLAUDE.md's Build section, and the memory file
  `no-local-builds-until-new-cpu.md`. `integrate.sh --rom` can stay.
- [ ] Rerun the parallel check (`C:\Users\Ian\oxide-flake-check\parallel.py`,
  and the same file from WSL). WSL failed about ten times as often as Windows
  under the same load, and the wedge may be a second, WSL-kernel problem that
  the CPU has been hiding.
- [ ] Build `oxide` locally once and compare its SHA-1 with GitHub's build of
  the same commit. Until they match, keep using `tools/oxide/fetch-rom`.

## 1. The ROMs and the save

- [ ] Fetch the ordinary ROM and the test kit ROM of the current `oxide`:
  `tools/oxide/fetch-rom <commit>` and `tools/oxide/fetch-rom --testkit <commit>`.
- [ ] **Start a new game.** An old save reads every ability as NONE by design
  (element 2 moved the field) and is no valid test bed.
- [ ] Known crash to avoid until the bug track fixes it: UNLOCK FPS set to
  ALWAYS hard-crashes on entering Sandgem Town (tracker, Phase 5).

## 2. The test kit ROM

The kit's NPC and menus are described in `docs/oxide/test-kit.md`, set by set,
with what each should show. The kit cannot set up double battles, a frozen
Pokemon, or a foe holding an item; those checks are marked for normal play.

- [ ] **Element 4, the move sets.** Sets 1 to 22 passed in rounds 1 to 3
  (2026-09-22 to 23). Still to see: sets 23 to 26; sets 27 to 31 (Sticky Web,
  After You, Aurora Veil, the four side guards against the kit's two new wild
  foes, and Belch with the Sitrus Berry the set gives), which the paged menu
  now reaches safely; and sets 32 to 41 on the "More sets" page (Electro Ball
  by Speed ratio, Stored Power, Retaliate, Echoed Voice, Stomping Tantrum,
  Last Respects, Hard Press, Pika Papow and Veevee Volley, Lash Out, Grav
  Apple). A stub effect does its damage and skips its extra, or says "But
  nothing happened!"; that is expected. Autotomize prints no "became nimble!",
  as Ian ruled.
- [ ] **Element 5, the Abilities menu** (two pages, Neutralizing Gas last): one
  entry per ability that shows itself, each with its own wild foe. For
  Neutralizing Gas: Galarian Weezing against a wild Chansey given Pressure
  shows the entry message as Weezing comes in, no extra PP is spent while the
  gas is out, and switching Weezing out prints the exit message followed by
  Chansey's Pressure message again.
- [ ] **The staples rulings, the Modern rules menu** (22 entries): Sturdy as a
  Focus Sash, Lightning Rod and Storm Drain immunity, the Intimidate blockers,
  Grass against powder, Electric against paralysis, 1.5x critical hits, Defog
  clearing hazards from both sides and screens only from the target's, Rapid
  Spin's Speed raise, and the rest the menu lists.
- [ ] **Native moves at modern numbers.** Fury Cutter used five times in a row
  goes 40, 80, 160, 160, 160 in power, so its damage stops growing after the
  third hit; Roar and Whirlwind never miss.
- [ ] **Fairy.** A Dragon move does nothing to Clefairy or Ralts, a Poison or
  Steel move does double, the summary screen reads FAIRY, and the Pokedex info
  page shows the NORMAL plate (the known gap) rather than garbage. The Poketch
  move tester agrees with the battle engine.
- [ ] **The Move Relearner and learnsets.** At the Move Relearner, no move name
  clips beyond the eight known ones, descriptions read sensibly in five lines,
  and a new species' moves are listed. Level a Pokemon through a move it should
  learn and confirm the right move at the right level (a wrong widening would
  be wrong for all 667 learnsets). A Rotom in a form, or a Giratina holding the
  Griseous Orb, shows its form's stats.
- [ ] **One calculator roll** (the encounter tool, M8): in a battle, note an
  attacker's and a defender's level and stats and the damage a move does, enter
  the same two in the encounter tool's calculator, and check the damage falls
  in its range.
- [ ] **Element 8, hidden abilities and restored items** (the last three
  Modern rules entries):
  "Hidden ability gift" gives a Lv. 15 Litten whose summary reads
  Intimidate, not Blaze; one Rare Candy makes a Torracat that still reads
  Intimidate. "Hidden ability wild" opens with the wild Litten's Intimidate
  lowering your lead's Attack; the flag clears itself after that one use.
  "Items restored": Mew eats its Sitrus Berry after Belly Drum, and has it
  back in its summary after the battle.

## 3. The ordinary ROM, early game (Twinleaf to Hearthome)

- [ ] Rare Candy chaining works.
- [ ] The options menu reads UNLOCK FPS, with OFF, BATTLE and ALWAYS (see the
  known crash above before choosing ALWAYS).
- [ ] Held items come back after battle (element 8): give a Pokemon an Oran or
  Sitrus Berry, let a trainer's Pokemon bring it below half so it eats the
  Berry, and after the battle its summary shows the Berry again. The same for
  a Focus Sash that saved it. The kit's "Items restored" entry shows it first.
- [ ] Battle style is always Set (element 8): the options menu shows SET
  highlighted and left and right do not move it, and when a trainer's Pokemon
  faints the game sends the next one out without asking whether you want to
  switch.
- [ ] Shinx's ability is always Rivalry, never Intimidate; Bidoof and Starly
  hatch in about 255 steps, down from about 3,825.
- [ ] Answering yes to "use another Repel?" works (the one carried-over thing
  that was broken and is fixed).
- [ ] A walk through a few bulk-generated maps, the gift houses first.
- [ ] Trainer gender: the ability and gender nibble is read as 1 male, 2 female,
  which is a guess no Route 202 trainer exercises; swap it if anything reads
  wrong.
- [ ] **(live)** The AI fix on Camper Zackary's first turn (level 15, a Castform
  with Rain Dance, a Weather-flag trainer): break at the end of
  `TrainerAI_MainSingles` and read `moveScore`. Rain Dance reads 105 and
  neither attack carries the Weather flag's +5 (compare the +5, not the gap).
- [ ] Honey trees at one badge: slather a tree and check the species and levels
  against table 1 of `res/field/encounters/encounters_honey_tree.json`. The
  Munchlax trees are gone.
- [ ] Valley Windworks: the Drifloon balloon no longer appears.
- [ ] The Hearthome Fan Club member only says goodbye, with no starter gift.
- [ ] After the overworld-sprite carry-over lands (tracker, Phase 3): the NPC
  outside Sandgem's Pokemon Center draws correctly, and so do the Clown-type
  NPCs on the other 34 maps that share that sprite slot.

## 4. The ordinary ROM, mid-game

- [ ] **(live)** Gardenia's Cherrim with Sunny Day: the same AI check as Camper
  Zackary's.
- [ ] Honey trees at five badges: check against table 5.
- [ ] Iron Island: Riley's egg hatches as a random species, one of eight lines.
- [ ] Snowpoint City: Mindy takes a Snover and gives a Suicune, which is shiny.
- [ ] **(live)** Worker Jackson's Wormadam-Trash (level 49, Relaxed, every IV 27)
  shows 131 HP, 85 Attack, 122 Defense, 85 Sp. Atk, 111 Sp. Def and 47 Speed.
- [ ] Galactic HQ, Saturn: the battle opens with "The dimensions became
  distorted!", the slower Pokemon moves first all fight, "The twisted dimensions
  returned to normal!" never appears, a Trick Room from either side fails, and
  Saturn's AI never chooses it.
- [ ] Once `main-scripts` merges: the Snowpoint ferry opens after Galactic HQ is
  cleared, Route 225 is open from the first arrival at the Fight Area, and the
  Volkner and Flint tag battle waits for the Beacon Badge. The legendary draws
  (Acuity Cavern, Mesprit's roamer, Heatran) as they land.
- [ ] **(live)** Volkner's battle: his Rotom-Mow (level 61, Modest, every IV 29)
  shows 149 HP, 90 Attack, 153 Defense, 165 Sp. Atk, 153 Sp. Def and 133 Speed.

## 5. The ordinary ROM, after the League

On a save with the National Dex and the game beaten:

- [ ] Acuity Lakefront's grass and the Poke Radar there give no Weavile,
  Abomasnow, Mamoswine or Glalie, and radar chains still build on the area's
  own species.
- [ ] The rival's younger sibling in Sandgem keeps her ordinary line when talked
  to twice.
- [ ] Sinnoh Now, watched a few times, shows no swarm news flash.
- [ ] The Great Marsh binoculars show only what the marsh can give.
- [ ] If a GBA game can be put in melonDS's second slot, no route gains its
  species.

## Passed

Ticked checks move here with the date they passed.
